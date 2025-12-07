"""
使用Selenium爬取全国农产品批发市场价格信息系统
针对需要JavaScript渲染的页面
"""
from typing import List, Dict
import logging
import json
import re
from datetime import datetime, date
from .base_spider import BaseSpider

logger = logging.getLogger(__name__)

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logger.warning("Selenium未安装，无法使用Selenium爬虫。安装命令: pip install selenium")


class PFSCSeleniumSpider(BaseSpider):
    """使用Selenium的爬虫（处理JavaScript渲染）"""
    
    def __init__(self):
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium未安装，请运行: pip install selenium")
        
        super().__init__(
            name='pfsc_selenium',
            base_url='https://pfsc.agri.cn'
        )
        self.driver = None
    
    def _init_driver(self):
        """初始化Selenium WebDriver"""
        if self.driver:
            return self.driver
        
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 无头模式
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # 尝试创建Chrome驱动
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except:
                # 如果Chrome不可用，尝试Edge
                try:
                    from selenium.webdriver.edge.options import Options as EdgeOptions
                    edge_options = EdgeOptions()
                    edge_options.add_argument('--headless')
                    self.driver = webdriver.Edge(options=edge_options)
                except:
                    raise Exception("未找到Chrome或Edge浏览器驱动")
            
            logger.info("Selenium WebDriver初始化成功")
            return self.driver
            
        except Exception as e:
            logger.error(f"初始化WebDriver失败: {str(e)}")
            raise
    
    def crawl(self) -> List[Dict]:
        """
        使用Selenium爬取数据
        """
        data_list = []
        
        if not SELENIUM_AVAILABLE:
            logger.error("Selenium未安装")
            return data_list
        
        try:
            driver = self._init_driver()
            url = f"{self.base_url}/#/priceMarket"
            
            logger.info(f"访问页面: {url}")
            driver.get(url)
            
            # 等待页面加载
            wait = WebDriverWait(driver, 20)
            
            # 方法1: 等待数据表格加载
            try:
                # 尝试多种可能的选择器
                selectors = [
                    "table",
                    ".price-table",
                    ".data-table",
                    "[class*='table']",
                    "[class*='price']",
                ]
                
                table = None
                for selector in selectors:
                    try:
                        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        if table:
                            logger.info(f"找到表格元素: {selector}")
                            break
                    except:
                        continue
                
                if table:
                    # 解析表格数据
                    data_list = self._parse_selenium_table(driver, table)
                
            except Exception as e:
                logger.debug(f"表格解析失败: {str(e)}")
            
            # 方法2: 从页面中提取JSON数据
            if not data_list:
                try:
                    page_source = driver.page_source
                    data_list = self._extract_json_from_page(page_source)
                except Exception as e:
                    logger.debug(f"JSON提取失败: {str(e)}")
            
            # 方法3: 执行JavaScript获取数据
            if not data_list:
                try:
                    data_list = self._execute_js_to_get_data(driver)
                except Exception as e:
                    logger.debug(f"JavaScript执行失败: {str(e)}")
            
            logger.info(f"总共获取 {len(data_list)} 条数据")
            
        except Exception as e:
            logger.error(f"Selenium爬取失败: {str(e)}", exc_info=True)
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
        
        return data_list
    
    def _parse_selenium_table(self, driver, table) -> List[Dict]:
        """解析Selenium找到的表格"""
        data_list = []
        
        try:
            rows = table.find_elements(By.TAG_NAME, "tr")
            if not rows:
                return data_list
            
            # 获取表头
            headers = []
            header_row = rows[0]
            header_cells = header_row.find_elements(By.TAG_NAME, "th")
            if not header_cells:
                header_cells = header_row.find_elements(By.TAG_NAME, "td")
            
            for cell in header_cells:
                headers.append(cell.text.strip())
            
            # 解析数据行
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3:
                    row_data = {}
                    for i, cell in enumerate(cells):
                        if i < len(headers):
                            row_data[headers[i]] = cell.text.strip()
                    
                    parsed = self._parse_table_row(row_data)
                    if parsed:
                        data_list.append(parsed)
        
        except Exception as e:
            logger.error(f"表格解析失败: {str(e)}")
        
        return data_list
    
    def _extract_json_from_page(self, page_source: str) -> List[Dict]:
        """从页面源码中提取JSON数据"""
        data_list = []
        
        try:
            # 查找可能的JSON数据
            patterns = [
                r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
                r'var\s+priceData\s*=\s*(\[.*?\]);',
                r'const\s+priceList\s*=\s*(\[.*?\]);',
                r'"data":\s*(\[.*?\])',
                r'priceMarket.*?=\s*(\[.*?\])',
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, page_source, re.DOTALL)
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
                if data_list:
                    break
        
        except Exception as e:
            logger.error(f"JSON提取失败: {str(e)}")
        
        return data_list
    
    def _execute_js_to_get_data(self, driver) -> List[Dict]:
        """执行JavaScript获取数据"""
        data_list = []
        
        try:
            # 尝试执行JavaScript获取数据
            js_code = """
            // 尝试多种方式获取数据
            var data = null;
            
            // 方法1: 从window对象获取
            if (window.priceData) {
                data = window.priceData;
            } else if (window.__INITIAL_STATE__) {
                data = window.__INITIAL_STATE__;
            } else if (window.app && window.app.$store) {
                data = window.app.$store.state;
            }
            
            return JSON.stringify(data);
            """
            
            result = driver.execute_script(js_code)
            if result and result != 'null':
                data_obj = json.loads(result)
                items = self._extract_items_from_json(data_obj)
                for item in items:
                    parsed = self._parse_item(item)
                    if parsed:
                        data_list.append(parsed)
        
        except Exception as e:
            logger.debug(f"JavaScript执行失败: {str(e)}")
        
        return data_list
    
    def _extract_items_from_json(self, data: any) -> List[Dict]:
        """从JSON数据中提取数据项列表"""
        items = []
        
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            for key in ['data', 'list', 'results', 'items', 'records', 'content', 'priceMarket', 'priceList']:
                if key in data and isinstance(data[key], list):
                    items = data[key]
                    break
            if not items and data:
                items = [data]
        
        return items
    
    def _parse_item(self, item: Dict) -> Dict:
        """解析单个数据项"""
        try:
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
            
            return {
                'product_name': str(product_name).strip(),
                'product_category': (
                    item.get('category') or 
                    item.get('categoryName') or 
                    item.get('product_category') or 
                    item.get('cplb') or
                    item.get('lb') or
                    '其他'
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
                    item.get('sj') or
                    date.today()
                ),
                'raw_content': json.dumps(item, ensure_ascii=False),
            }
        except Exception as e:
            logger.debug(f"解析数据项失败: {str(e)}")
            return None
    
    def _parse_table_row(self, row_data: Dict) -> Dict:
        """解析表格行数据"""
        try:
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
                'product_category': '其他',
                'price': self._parse_price(price_str),
                'unit': self._extract_unit(price_str),
                'market_name': row_data.get('市场', row_data.get('市场名称', '')),
                'region': row_data.get('地区', row_data.get('区域', '')),
                'date': date.today(),
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
    
    def _parse_date(self, date_str) -> date:
        """解析日期"""
        if isinstance(date_str, date):
            return date_str
        if not date_str:
            return date.today()
        
        try:
            formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d', '%Y-%m-%d %H:%M:%S', '%Y年%m月%d日']
            for fmt in formats:
                try:
                    return datetime.strptime(str(date_str), fmt).date()
                except:
                    continue
        except:
            pass
        
        return date.today()

