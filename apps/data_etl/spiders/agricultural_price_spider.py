"""
农产品价格爬虫 - 针对 pfsc.agri.cn 全国农产品批发市场价格信息系统
"""
from typing import List, Dict
from .base_spider import BaseSpider
import logging
import json
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AgriculturalPriceSpider(BaseSpider):
    """农产品价格爬虫 - 针对全国农产品批发市场价格信息系统"""
    
    def __init__(self):
        # 更新请求头，模拟真实浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://pfsc.agri.cn/',
            'Origin': 'https://pfsc.agri.cn'
        }
        super().__init__(
            name='agricultural_price',
            base_url='https://pfsc.agri.cn',
            headers=headers
        )
    
    def crawl(self) -> List[Dict]:
        """
        爬取农产品价格数据
        :return: 数据列表
        """
        data_list = []
        
        try:
            # 方法1: 尝试直接调用API接口
            api_data = self._fetch_from_api()
            if api_data:
                data_list.extend(api_data)
                logger.info(f"从API获取到 {len(api_data)} 条数据")
            
            # 方法2: 如果API失败，尝试解析HTML页面
            if not data_list:
                html_data = self._fetch_from_html()
                if html_data:
                    data_list.extend(html_data)
                    logger.info(f"从HTML获取到 {len(html_data)} 条数据")
            
            logger.info(f"总共爬取到 {len(data_list)} 条数据")
            
        except Exception as e:
            logger.error(f"爬取失败: {str(e)}", exc_info=True)
        
        return data_list
    
    def _fetch_from_api(self) -> List[Dict]:
        """
        尝试从API接口获取数据
        """
        data_list = []
        
        # 常见的API端点（需要根据实际网站调整）
        api_endpoints = [
            '/api/priceMarket/list',
            '/api/price/list',
            '/api/market/price',
            '/api/v1/priceMarket',
        ]
        
        # 尝试不同的API端点
        for endpoint in api_endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                
                # 设置请求参数（根据实际API调整）
                params = {
                    'page': 1,
                    'pageSize': 100,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                }
                
                response = self.fetch(url, params=params)
                if response and response.status_code == 200:
                    try:
                        result = response.json()
                        # 解析JSON数据（根据实际API响应结构调整）
                        if isinstance(result, dict):
                            items = result.get('data', result.get('list', result.get('results', [])))
                        elif isinstance(result, list):
                            items = result
                        else:
                            items = []
                        
                        for item in items:
                            data = self._parse_api_item(item)
                            if data:
                                data_list.append(data)
                        
                        if data_list:
                            logger.info(f"成功从API端点 {endpoint} 获取数据")
                            break
                    except json.JSONDecodeError:
                        continue
            except Exception as e:
                logger.debug(f"尝试API端点 {endpoint} 失败: {str(e)}")
                continue
        
        return data_list
    
    def _fetch_from_html(self) -> List[Dict]:
        """
        从HTML页面解析数据（备用方案）
        """
        data_list = []
        
        try:
            url = f"{self.base_url}/#/priceMarket"
            response = self.fetch(url)
            if not response:
                return data_list
            
            soup = self.parse_html(response.text)
            
            # 方法1: 查找包含JSON数据的script标签
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # 尝试提取JSON数据
                    json_match = re.search(r'var\s+priceData\s*=\s*(\[.*?\]);', script.string, re.DOTALL)
                    if json_match:
                        try:
                            json_str = json_match.group(1)
                            items = json.loads(json_str)
                            for item in items:
                                data = self._parse_html_item(item)
                                if data:
                                    data_list.append(data)
                            break
                        except:
                            continue
            
            # 方法2: 解析表格数据
            if not data_list:
                tables = soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')[1:]  # 跳过表头
                    for row in rows:
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 4:
                            data = {
                                'product_name': self.extract_text(cols[0]),
                                'product_category': self._extract_category(self.extract_text(cols[0])),
                                'price': self._parse_price(self.extract_text(cols[1])),
                                'unit': self._extract_unit(self.extract_text(cols[1])),
                                'market_name': self.extract_text(cols[2]) if len(cols) > 2 else '',
                                'region': self.extract_text(cols[3]) if len(cols) > 3 else '',
                                'date': datetime.now().date(),
                                'raw_content': str(row),
                            }
                            if data['product_name'] and data['price'] > 0:
                                data_list.append(data)
            
        except Exception as e:
            logger.error(f"HTML解析失败: {str(e)}")
        
        return data_list
    
    def _parse_api_item(self, item: Dict) -> Dict:
        """
        解析API返回的数据项
        """
        try:
            # 根据实际API响应结构调整字段映射
            data = {
                'product_name': item.get('productName') or item.get('name') or item.get('product_name') or item.get('cpmc', ''),
                'product_category': item.get('category') or item.get('categoryName') or item.get('product_category') or item.get('cplb', ''),
                'price': self._parse_price_value(item.get('price') or item.get('jg') or item.get('priceValue', 0)),
                'unit': item.get('unit') or item.get('dw') or item.get('priceUnit', '元/斤'),
                'market_name': item.get('marketName') or item.get('market') or item.get('market_name') or item.get('scmc', ''),
                'region': item.get('region') or item.get('area') or item.get('regionName') or item.get('dq', ''),
                'date': self._parse_date(item.get('date') or item.get('rq') or item.get('priceDate')),
                'raw_content': json.dumps(item, ensure_ascii=False),
            }
            
            # 验证必要字段
            if data['product_name'] and data['price'] > 0:
                return data
        except Exception as e:
            logger.debug(f"解析API数据项失败: {str(e)}")
        
        return None
    
    def _parse_html_item(self, item: Dict) -> Dict:
        """
        解析HTML中的JSON数据项
        """
        return self._parse_api_item(item)
    
    def _parse_price(self, price_str: str) -> float:
        """
        解析价格字符串
        """
        try:
            # 移除货币符号、单位和空格
            price_str = re.sub(r'[¥￥元/斤公斤kg]', '', str(price_str))
            price_str = price_str.strip()
            # 提取数字
            match = re.search(r'(\d+\.?\d*)', price_str)
            if match:
                return float(match.group(1))
        except:
            pass
        return 0.0
    
    def _parse_price_value(self, value) -> float:
        """
        解析价格值（可能是字符串或数字）
        """
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            return self._parse_price(value)
        return 0.0
    
    def _extract_unit(self, text: str) -> str:
        """
        从文本中提取单位
        """
        units = ['元/斤', '元/公斤', '元/kg', '元/吨']
        for unit in units:
            if unit in text:
                return unit
        return '元/斤'  # 默认单位
    
    def _extract_category(self, product_name: str) -> str:
        """
        根据产品名称推断类别
        """
        categories = {
            '水果': ['苹果', '香蕉', '橙子', '葡萄', '西瓜', '梨', '桃', '草莓', '樱桃'],
            '蔬菜': ['白菜', '萝卜', '土豆', '西红柿', '黄瓜', '茄子', '辣椒', '芹菜'],
            '粮食': ['大米', '小麦', '玉米', '大豆', '花生'],
            '肉类': ['猪肉', '牛肉', '羊肉', '鸡肉', '鸭肉'],
        }
        
        for category, products in categories.items():
            for product in products:
                if product in product_name:
                    return category
        return '其他'
    
    def _parse_date(self, date_str) -> datetime.date:
        """
        解析日期字符串
        """
        if not date_str:
            return datetime.now().date()
        
        try:
            # 尝试多种日期格式
            formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d', '%Y-%m-%d %H:%M:%S']
            for fmt in formats:
                try:
                    return datetime.strptime(str(date_str), fmt).date()
                except:
                    continue
        except:
            pass
        
        return datetime.now().date()

