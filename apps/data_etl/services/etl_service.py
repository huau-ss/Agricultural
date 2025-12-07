"""
ETL服务 - 数据采集、清洗、入库
"""
import logging
from datetime import datetime
from typing import List, Dict
from django.utils import timezone
from apps.data_etl.models import DataSource, RawData, CleanedData, ETLTask
from apps.data_etl.spiders.agricultural_price_spider import AgriculturalPriceSpider
from apps.data_etl.spiders.pfsc_spider import PFSCSpider
from utils.data_standardization import DataStandardizer

logger = logging.getLogger(__name__)


class ETLService:
    """ETL服务类"""
    
    def __init__(self):
        self.standardizer = DataStandardizer()
    
    def run_etl_task(self, source_id: int, task_name: str = None) -> ETLTask:
        """
        执行ETL任务
        :param source_id: 数据源ID
        :param task_name: 任务名称
        :return: ETL任务对象
        """
        try:
            source = DataSource.objects.get(id=source_id, status='active')
            
            # 创建任务记录
            task = ETLTask.objects.create(
                task_name=task_name or f"ETL任务-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                source=source,
                status='running'
            )
            
            # 1. 数据采集
            raw_data_list = self._extract(source)
            task.total_count = len(raw_data_list)
            
            # 2. 数据清洗和转换
            success_count = 0
            failed_count = 0
            
            for raw_item in raw_data_list:
                try:
                    cleaned_data = self._transform(raw_item, source)
                    if cleaned_data:
                        success_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    logger.error(f"数据清洗失败: {str(e)}")
                    failed_count += 1
            
            # 3. 更新任务状态
            task.success_count = success_count
            task.failed_count = failed_count
            task.status = 'success' if failed_count == 0 else 'success'  # 部分成功也算成功
            task.finished_at = timezone.now()
            task.save()
            
            logger.info(f"ETL任务完成: {task.task_name}, 成功: {success_count}, 失败: {failed_count}")
            
            return task
            
        except DataSource.DoesNotExist:
            raise ValueError(f"数据源不存在: {source_id}")
        except Exception as e:
            if 'task' in locals():
                task.status = 'failed'
                task.error_message = str(e)
                task.finished_at = timezone.now()
                task.save()
            logger.error(f"ETL任务失败: {str(e)}")
            raise
    
    def _extract(self, source: DataSource) -> List[Dict]:
        """
        数据提取（爬虫）
        :param source: 数据源对象
        :return: 原始数据列表
        """
        raw_data_list = []
        
        try:
            # 根据数据源类型选择不同的爬虫
            if source.source_type == 'web':
                # 根据URL判断使用哪个爬虫
                if 'pfsc.agri.cn' in source.url or 'agri.cn' in source.url:
                    # 先尝试普通爬虫
                    spider = PFSCSpider()
                    data_list = spider.crawl()
                    
                    # 如果普通爬虫失败，尝试Selenium（需要安装selenium）
                    if not data_list:
                        try:
                            from apps.data_etl.spiders.pfsc_selenium_spider import PFSCSeleniumSpider
                            logger.info("尝试使用Selenium爬虫...")
                            selenium_spider = PFSCSeleniumSpider()
                            data_list = selenium_spider.crawl()
                        except ImportError:
                            logger.warning("Selenium未安装，无法使用Selenium爬虫")
                        except Exception as e:
                            logger.error(f"Selenium爬虫失败: {str(e)}")
                else:
                    spider = AgriculturalPriceSpider()
                    data_list = spider.crawl()
                
                # 保存原始数据
                for item in data_list:
                    raw_data = RawData.objects.create(
                        source=source,
                        product_name=item.get('product_name', ''),
                        product_category=item.get('product_category', ''),
                        price=item.get('price', 0),
                        unit=item.get('unit', '元/斤'),
                        market_name=item.get('market_name', ''),
                        region=item.get('region', ''),
                        date=item.get('date', datetime.now().date()),
                        raw_content=item.get('raw_content', ''),
                        status='pending'
                    )
                    raw_data_list.append({
                        'id': raw_data.id,
                        'data': item
                    })
            
            elif source.source_type == 'api':
                # TODO: 实现API数据源
                pass
            
            elif source.source_type == 'file':
                # TODO: 实现文件导入
                pass
            
        except Exception as e:
            logger.error(f"数据提取失败: {str(e)}")
        
        return raw_data_list
    
    def _transform(self, raw_item: Dict, source: DataSource) -> CleanedData:
        """
        数据转换和清洗
        :param raw_item: 原始数据项
        :param source: 数据源对象
        :return: 清洗后的数据对象
        """
        try:
            raw_data_id = raw_item['id']
            item = raw_item['data']
            
            raw_data = RawData.objects.get(id=raw_data_id)
            
            # 数据标准化
            standardized_data = self.standardizer.standardize(item)
            
            # 数据质量评分
            quality_score = self.standardizer.calculate_quality_score(standardized_data)
            
            # 创建清洗数据
            cleaned_data = CleanedData.objects.create(
                raw_data=raw_data,
                product_name=standardized_data.get('product_name', ''),
                product_category=standardized_data.get('product_category', ''),
                price=standardized_data.get('price', 0),
                unit=standardized_data.get('unit', '元/斤'),
                market_name=standardized_data.get('market_name', ''),
                region=standardized_data.get('region', ''),
                date=standardized_data.get('date', datetime.now().date()),
                quality_score=quality_score
            )
            
            # 更新原始数据状态
            raw_data.status = 'cleaned'
            raw_data.save()
            
            # 同步到市场价格表
            self._load_to_market(cleaned_data)
            
            return cleaned_data
            
        except Exception as e:
            logger.error(f"数据转换失败: {str(e)}")
            if 'raw_data' in locals():
                raw_data.status = 'error'
                raw_data.save()
            return None
    
    def _load_to_market(self, cleaned_data: CleanedData):
        """
        加载到市场价格表
        :param cleaned_data: 清洗后的数据
        """
        from apps.market.models import MarketPrice
        
        try:
            # 检查是否已存在
            market_price, created = MarketPrice.objects.get_or_create(
                product_name=cleaned_data.product_name,
                market_name=cleaned_data.market_name,
                date=cleaned_data.date,
                defaults={
                    'product_category': cleaned_data.product_category,
                    'price': cleaned_data.price,
                    'unit': cleaned_data.unit,
                    'region': cleaned_data.region,
                }
            )
            
            if not created:
                # 计算价格变化
                old_price = market_price.price
                new_price = cleaned_data.price
                market_price.price = new_price
                market_price.price_change = new_price - old_price
                if old_price > 0:
                    market_price.price_change_rate = ((new_price - old_price) / old_price) * 100
                market_price.save()
            
        except Exception as e:
            logger.error(f"加载到市场价格表失败: {str(e)}")

