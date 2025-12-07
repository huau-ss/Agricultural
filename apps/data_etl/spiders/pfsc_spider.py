"""
全国农产品批发市场价格信息系统爬虫
针对 https://pfsc.agri.cn/#/priceMarket
"""
from typing import List, Dict
import logging
import json
import re
from datetime import datetime
from .base_spider import BaseSpider

logger = logging.getLogger(__name__)


class PFSCSpider(BaseSpider):
    """全国农产品批发市场价格信息系统爬虫"""
    
    def __init__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://pfsc.agri.cn/',
            'Origin': 'https://pfsc.agri.cn'
        }
        super().__init__(
            name='pfsc_agri',
            base_url='https://pfsc.agri.cn',
            headers=headers
        )
    
    def crawl(self) -> List[Dict]:
        """
        爬取农产品价格数据
        """
        data_list = []
        
        try:
            # 方法1: 优先尝试真实的API接口
            api_data = self._try_api_endpoints()
            if api_data:
                data_list.extend(api_data)
                logger.info(f"从API获取到 {len(api_data)} 条数据")
                return data_list  # 如果API成功，直接返回
            
            # 方法2: 如果API失败，尝试从主页面获取数据
            main_page_data = self._try_main_page()
            if main_page_data:
                data_list.extend(main_page_data)
                logger.info(f"从主页面获取到 {len(main_page_data)} 条数据")
            
            # 方法3: 尝试解析HTML页面
            if not data_list:
                page_data = self._try_parse_page()
                if page_data:
                    data_list.extend(page_data)
                    logger.info(f"从页面获取到 {len(page_data)} 条数据")
            
            # 方法4: 尝试使用Selenium（如果安装了）
            if not data_list:
                selenium_data = self._try_selenium()
                if selenium_data:
                    data_list.extend(selenium_data)
                    logger.info(f"使用Selenium获取到 {len(selenium_data)} 条数据")
            
            if not data_list:
                logger.warning("所有方法都失败，无法获取真实数据")
                raise Exception("无法从网站获取数据，请检查网站结构或网络连接")
            
            logger.info(f"总共获取 {len(data_list)} 条真实数据")
            
        except Exception as e:
            logger.error(f"爬取失败: {str(e)}", exc_info=True)
            raise  # 不生成测试数据，直接抛出异常
        
        return data_list
    
    def _try_api_endpoints(self) -> List[Dict]:
        """尝试真实的API端点"""
        data_list = []
        
        try:
            # 真实的API端点
            url = f"{self.base_url}/api/priceQuotationController/pageList"
            
            # 更新请求头
            headers = self.headers.copy()
            headers.update({
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            })
            
            # 分页获取所有数据
            page_num = 1
            page_size = 100  # 每页100条
            max_pages = 100  # 最多获取100页，防止无限循环
            
            while page_num <= max_pages:
                # 请求参数
                payload = {
                    'pageNum': page_num,
                    'pageSize': page_size,
                    'marketId': '',
                    'provinceCode': '',
                    'pid': '',
                    'varietyId': ''
                }
                
                try:
                    response = self.session.post(
                        url,
                        json=payload,
                        headers=headers,
                        timeout=30
                    )
                    
                    if response and response.status_code == 200:
                        result = response.json()
                        
                        # 检查响应状态
                        if result.get('code') != 200:
                            logger.warning(f"API返回错误: {result.get('message', '未知错误')}")
                            break
                        
                        # 提取数据列表
                        content = result.get('content', {})
                        items = content.get('list', [])
                        
                        if not items:
                            logger.info("没有更多数据")
                            break
                        
                        # 解析数据
                        page_data_count = 0
                        for item in items:
                            parsed = self._parse_pfsc_item(item)
                            if parsed:
                                data_list.append(parsed)
                                page_data_count += 1
                        
                        logger.info(f"第 {page_num} 页获取到 {page_data_count} 条数据")
                        
                        # 检查是否还有下一页
                        if not content.get('hasNextPage', False):
                            break
                        
                        page_num += 1
                        self.sleep(0.5)  # 避免请求过快
                        
                    elif response and response.status_code == 401:
                        logger.warning("API需要认证，可能需要登录或token")
                        break
                    else:
                        logger.warning(f"请求失败，状态码: {response.status_code if response else 'None'}")
                        break
                        
                except Exception as e:
                    logger.error(f"请求第 {page_num} 页失败: {str(e)}")
                    break
            
            if data_list:
                logger.info(f"成功从API获取 {len(data_list)} 条数据")
            else:
                logger.warning("未能从API获取到数据")
        
        except Exception as e:
            logger.error(f"API请求失败: {str(e)}", exc_info=True)
        
        return data_list
    
    def _try_main_page(self) -> List[Dict]:
        """尝试从主页面获取初始数据"""
        data_list = []
        
        try:
            # 访问主页面
            url = f"{self.base_url}/"
            response = self.fetch(url)
            if not response:
                return data_list
            
            html = response.text
            logger.info(f"成功获取主页面，长度: {len(html)}")
            
            # 查找可能的API端点或数据
            # 很多SPA应用会在HTML中暴露API端点
            api_patterns = [
                r'api[_-]?url["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'baseURL["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'["\'](/api/[^"\']+)["\']',
            ]
            
            for pattern in api_patterns:
                matches = re.finditer(pattern, html, re.IGNORECASE)
                for match in matches:
                    api_path = match.group(1)
                    if 'price' in api_path.lower() or 'market' in api_path.lower():
                        logger.info(f"发现可能的API路径: {api_path}")
                        # 尝试调用这个API
                        try:
                            api_url = f"{self.base_url}{api_path}" if not api_path.startswith('http') else api_path
                            api_response = self.fetch(api_url)
                            if api_response and api_response.status_code == 200:
                                result = api_response.json()
                                items = self._extract_items_from_json(result)
                                for item in items:
                                    parsed = self._parse_item(item)
                                    if parsed:
                                        data_list.append(parsed)
                                if data_list:
                                    return data_list
                        except:
                            continue
            
            # 查找内嵌的JSON数据
            json_patterns = [
                r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
                r'window\.__PRELOADED_STATE__\s*=\s*({.*?});',
                r'var\s+priceData\s*=\s*(\[.*?\]);',
                r'const\s+priceList\s*=\s*(\[.*?\]);',
                r'"priceMarket"[^}]*"data"\s*:\s*(\[.*?\])',
            ]
            
            for pattern in json_patterns:
                matches = re.finditer(pattern, html, re.DOTALL)
                for match in matches:
                    try:
                        json_str = match.group(1)
                        data_obj = json.loads(json_str)
                        items = self._extract_items_from_json(data_obj)
                        for item in items:
                            parsed = self._parse_item(item)
                            if parsed:
                                data_list.append(parsed)
                        if data_list:
                            logger.info("从主页面内嵌数据中提取到数据")
                            return data_list
                    except:
                        continue
            
        except Exception as e:
            logger.debug(f"主页面解析失败: {str(e)}")
        
        return data_list
    
    def _try_parse_page(self) -> List[Dict]:
        """尝试从HTML页面解析数据"""
        data_list = []
        
        try:
            # 尝试访问价格市场页面
            url = f"{self.base_url}/#/priceMarket"
            response = self.fetch(url)
            if not response:
                return data_list
            
            html = response.text
            logger.info(f"成功获取价格市场页面，长度: {len(html)}")
            
            # 方法1: 查找内嵌的JSON数据
            json_patterns = [
                r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
                r'var\s+priceData\s*=\s*(\[.*?\]);',
                r'const\s+priceList\s*=\s*(\[.*?\]);',
                r'"data":\s*(\[.*?\])',
            ]
            
            for pattern in json_patterns:
                matches = re.finditer(pattern, html, re.DOTALL)
                for match in matches:
                    try:
                        json_str = match.group(1)
                        data_obj = json.loads(json_str)
                        items = self._extract_items_from_json(data_obj)
                        for item in items:
                            parsed = self._parse_item(item)
                            if parsed:
                                data_list.append(parsed)
                        if data_list:
                            break
                    except:
                        continue
            
            # 方法2: 解析HTML表格
            if not data_list:
                soup = self.parse_html(html)
                tables = soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    headers = []
                    if rows:
                        header_row = rows[0]
                        headers = [self.extract_text(th) for th in header_row.find_all(['th', 'td'])]
                    
                    for row in rows[1:]:
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 3:
                            row_data = {}
                            for i, col in enumerate(cols):
                                if i < len(headers):
                                    row_data[headers[i]] = self.extract_text(col)
                            
                            parsed = self._parse_table_row(row_data)
                            if parsed:
                                data_list.append(parsed)
            
        except Exception as e:
            logger.error(f"页面解析失败: {str(e)}")
        
        return data_list
    
    def _try_selenium(self) -> List[Dict]:
        """尝试使用Selenium获取动态渲染的数据"""
        data_list = []
        
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            import time
            
            logger.info("尝试使用Selenium获取数据...")
            
            # 配置Chrome选项
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 无头模式
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                # 访问页面
                url = f"{self.base_url}/#/priceMarket"
                driver.get(url)
                
                # 等待页面加载
                time.sleep(5)
                
                # 尝试多种方式获取数据
                # 方法1: 查找表格数据
                try:
                    tables = driver.find_elements(By.TAG_NAME, 'table')
                    for table in tables:
                        rows = table.find_elements(By.TAG_NAME, 'tr')
                        if len(rows) > 1:
                            headers = [th.text for th in rows[0].find_elements(By.TAG_NAME, 'th')]
                            for row in rows[1:]:
                                cols = row.find_elements(By.TAG_NAME, 'td')
                                if len(cols) >= 3:
                                    row_data = {}
                                    for i, col in enumerate(cols):
                                        if i < len(headers):
                                            row_data[headers[i]] = col.text
                                    parsed = self._parse_table_row(row_data)
                                    if parsed:
                                        data_list.append(parsed)
                except:
                    pass
                
                # 方法2: 从网络请求中获取数据
                try:
                    logs = driver.get_log('performance')
                    for log in logs:
                        message = json.loads(log['message'])
                        if message['message']['method'] == 'Network.responseReceived':
                            response_url = message['message']['params']['response']['url']
                            if 'api' in response_url.lower() and ('price' in response_url.lower() or 'market' in response_url.lower()):
                                logger.info(f"发现API响应: {response_url}")
                                # 可以尝试获取响应内容
                except:
                    pass
                
                # 方法3: 执行JavaScript获取数据
                try:
                    js_data = driver.execute_script("""
                        // 尝试从window对象获取数据
                        if (window.priceData) return window.priceData;
                        if (window.__INITIAL_STATE__) return window.__INITIAL_STATE__;
                        if (window.app && window.app.$store && window.app.$store.state) {
                            return window.app.$store.state;
                        }
                        return null;
                    """)
                    if js_data:
                        items = self._extract_items_from_json(js_data)
                        for item in items:
                            parsed = self._parse_item(item)
                            if parsed:
                                data_list.append(parsed)
                except:
                    pass
                
            finally:
                driver.quit()
            
            if data_list:
                logger.info(f"使用Selenium获取到 {len(data_list)} 条数据")
            
        except ImportError:
            logger.warning("Selenium未安装，跳过Selenium方法。安装命令: pip install selenium")
        except Exception as e:
            logger.debug(f"Selenium方法失败: {str(e)}")
        
        return data_list
    
    def _generate_test_data(self) -> List[Dict]:
        """
        生成测试数据（当无法从网站获取数据时使用）
        """
        from datetime import date, timedelta
        import random
        
        logger.info("生成测试数据...")
        
        products = [
            {'name': '苹果', 'category': '水果', 'base_price': 8.5},
            {'name': '香蕉', 'category': '水果', 'base_price': 6.0},
            {'name': '橙子', 'category': '水果', 'base_price': 7.5},
            {'name': '葡萄', 'category': '水果', 'base_price': 12.0},
            {'name': '西瓜', 'category': '水果', 'base_price': 3.5},
            {'name': '白菜', 'category': '蔬菜', 'base_price': 2.5},
            {'name': '萝卜', 'category': '蔬菜', 'base_price': 2.0},
            {'name': '土豆', 'category': '蔬菜', 'base_price': 3.0},
            {'name': '西红柿', 'category': '蔬菜', 'base_price': 5.5},
            {'name': '黄瓜', 'category': '蔬菜', 'base_price': 4.0},
        ]
        
        regions = ['北京', '上海', '广州', '深圳', '杭州', '成都']
        markets = ['新发地市场', '江桥市场', '江南市场', '海吉星市场', '农副产品市场', '批发市场']
        
        data_list = []
        today = date.today()
        
        # 生成最近7天的数据
        for day_offset in range(7):
            data_date = today - timedelta(days=day_offset)
            
            for product in products:
                for region in regions[:3]:  # 每个产品生成3个地区的数据
                    # 价格波动 ±20%
                    price_variation = random.uniform(-0.2, 0.2)
                    price = product['base_price'] * (1 + price_variation)
                    price = round(price, 2)
                    
                    market = random.choice(markets)
                    
                    data = {
                        'product_name': product['name'],
                        'product_category': product['category'],
                        'price': price,
                        'unit': '元/斤',
                        'market_name': f'{region}{market}',
                        'region': region,
                        'date': data_date,
                        'raw_content': f"测试数据-{product['name']}-{region}-{data_date}"
                    }
                    data_list.append(data)
        
        logger.info(f"生成了 {len(data_list)} 条测试数据")
        return data_list
    
    def _extract_items_from_json(self, data: any) -> List[Dict]:
        """从JSON数据中提取数据项列表"""
        items = []
        
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            # 尝试常见的键名
            for key in ['data', 'list', 'results', 'items', 'records', 'content']:
                if key in data and isinstance(data[key], list):
                    items = data[key]
                    break
            
            # 如果没有找到列表，尝试将整个dict作为一项
            if not items and data:
                items = [data]
        
        return items
    
    def _parse_pfsc_item(self, item: Dict) -> Dict:
        """解析pfsc.agri.cn API返回的数据项"""
        try:
            # 根据实际API响应结构解析
            product_name = item.get('varietyName', '').strip()
            if not product_name:
                return None
            
            # 使用中间价作为价格
            price_str = item.get('middlePrice', '0')
            if not price_str or price_str == '0':
                # 如果没有中间价，使用最高价和最低价的平均值
                min_price = float(item.get('minimumPrice', 0) or 0)
                max_price = float(item.get('highestPrice', 0) or 0)
                if min_price > 0 and max_price > 0:
                    price_value = (min_price + max_price) / 2
                else:
                    price_value = max(min_price, max_price)
            else:
                price_value = float(price_str)
            
            if price_value <= 0:
                return None
            
            # 单位转换：元/公斤 -> 元/斤（除以2）
            unit = item.get('meteringUnit', '元/公斤')
            if '公斤' in unit or 'kg' in unit.lower():
                price_value = price_value / 2  # 转换为元/斤
                unit = '元/斤'
            elif '斤' not in unit:
                unit = '元/斤'  # 默认单位
            
            # 解析日期
            report_time = item.get('reportTime', '')
            if not report_time:
                report_time = item.get('inStorageTime', '')
            
            data = {
                'product_name': product_name,
                'product_category': item.get('varietyTypeName', '其他'),
                'price': round(price_value, 2),
                'unit': unit,
                'market_name': item.get('marketName', ''),
                'region': item.get('provinceName', '') or item.get('areaName', ''),
                'date': self._parse_date(report_time),
                'raw_content': json.dumps(item, ensure_ascii=False),
            }
            
            # 验证数据有效性
            if data['product_name'] and data['price'] > 0:
                return data
            
        except Exception as e:
            logger.debug(f"解析数据项失败: {str(e)}")
        
        return None
    
    def _parse_item(self, item: Dict) -> Dict:
        """解析单个数据项（通用方法，保留兼容性）"""
        # 优先使用pfsc专用解析方法
        if 'varietyName' in item or 'varietyId' in item:
            return self._parse_pfsc_item(item)
        
        # 否则使用通用解析方法
        try:
            # 字段映射（根据实际API响应调整）
            product_name = (
                item.get('productName') or 
                item.get('name') or 
                item.get('product_name') or 
                item.get('cpmc') or
                item.get('cpm') or
                ''
            )
            
            price_value = (
                item.get('price') or 
                item.get('jg') or 
                item.get('priceValue') or
                item.get('dj') or
                0
            )
            
            if not product_name or not price_value:
                return None
            
            data = {
                'product_name': str(product_name).strip(),
                'product_category': (
                    item.get('category') or 
                    item.get('categoryName') or 
                    item.get('product_category') or 
                    item.get('cplb') or
                    item.get('lb') or
                    self._infer_category(str(product_name))
                ),
                'price': self._parse_price_value(price_value),
                'unit': (
                    item.get('unit') or 
                    item.get('dw') or 
                    item.get('priceUnit') or
                    item.get('jldw') or
                    '元/斤'
                ),
                'market_name': (
                    item.get('marketName') or 
                    item.get('market') or 
                    item.get('market_name') or
                    item.get('scmc') or
                    item.get('sc') or
                    ''
                ),
                'region': (
                    item.get('region') or 
                    item.get('area') or 
                    item.get('regionName') or
                    item.get('dq') or
                    item.get('province') or
                    ''
                ),
                'date': self._parse_date(
                    item.get('date') or 
                    item.get('rq') or 
                    item.get('priceDate') or
                    item.get('sj')
                ),
                'raw_content': json.dumps(item, ensure_ascii=False),
            }
            
            # 验证数据有效性
            if data['product_name'] and data['price'] > 0:
                return data
            
        except Exception as e:
            logger.debug(f"解析数据项失败: {str(e)}")
        
        return None
    
    def _parse_table_row(self, row_data: Dict) -> Dict:
        """解析表格行数据"""
        try:
            # 尝试从表格数据中提取字段
            product_name = ''
            price_str = ''
            
            for key, value in row_data.items():
                key_lower = key.lower()
                if '产品' in key or '名称' in key or '品名' in key:
                    product_name = str(value).strip()
                elif '价格' in key or '价' in key:
                    price_str = str(value).strip()
            
            if not product_name or not price_str:
                return None
            
            return {
                'product_name': product_name,
                'product_category': self._infer_category(product_name),
                'price': self._parse_price(price_str),
                'unit': self._extract_unit(price_str),
                'market_name': row_data.get('市场', row_data.get('市场名称', '')),
                'region': row_data.get('地区', row_data.get('区域', '')),
                'date': datetime.now().date(),
                'raw_content': str(row_data),
            }
        except:
            return None
    
    def _parse_price_value(self, value) -> float:
        """解析价格值"""
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            return self._parse_price(value)
        return 0.0
    
    def _parse_price(self, price_str: str) -> float:
        """解析价格字符串"""
        try:
            price_str = re.sub(r'[¥￥元/斤公斤kg吨]', '', str(price_str))
            price_str = price_str.strip()
            match = re.search(r'(\d+\.?\d*)', price_str)
            if match:
                return float(match.group(1))
        except:
            pass
        return 0.0
    
    def _extract_unit(self, text: str) -> str:
        """提取单位"""
        units = ['元/斤', '元/公斤', '元/kg', '元/吨', '元/千克']
        for unit in units:
            if unit in text:
                return unit
        return '元/斤'
    
    def _infer_category(self, product_name: str) -> str:
        """根据产品名称推断类别"""
        categories = {
            '水果': ['苹果', '香蕉', '橙子', '葡萄', '西瓜', '梨', '桃', '草莓', '樱桃', '荔枝', '芒果'],
            '蔬菜': ['白菜', '萝卜', '土豆', '西红柿', '黄瓜', '茄子', '辣椒', '芹菜', '菠菜', '韭菜'],
            '粮食': ['大米', '小麦', '玉米', '大豆', '花生', '绿豆', '红豆'],
            '肉类': ['猪肉', '牛肉', '羊肉', '鸡肉', '鸭肉', '鱼肉'],
            '禽蛋': ['鸡蛋', '鸭蛋', '鹅蛋'],
        }
        
        for category, products in categories.items():
            for product in products:
                if product in product_name:
                    return category
        return '其他'
    
    def _parse_date(self, date_str) -> datetime.date:
        """解析日期"""
        if not date_str:
            return datetime.now().date()
        
        try:
            formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d', '%Y-%m-%d %H:%M:%S', '%Y年%m月%d日']
            for fmt in formats:
                try:
                    return datetime.strptime(str(date_str), fmt).date()
                except:
                    continue
        except:
            pass
        
        return datetime.now().date()

