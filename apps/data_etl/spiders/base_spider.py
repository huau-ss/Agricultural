"""
基础爬虫类
"""
import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class BaseSpider:
    """基础爬虫类"""
    
    def __init__(self, name: str, base_url: str, headers: Optional[Dict] = None):
        """
        初始化爬虫
        :param name: 爬虫名称
        :param base_url: 基础URL
        :param headers: 请求头
        """
        self.name = name
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """
        发送HTTP请求
        :param url: 请求URL
        :param method: 请求方法
        :param kwargs: 其他请求参数
        :return: 响应对象
        """
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=30, **kwargs)
            else:
                response = self.session.post(url, timeout=30, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"请求失败: {url}, 错误: {str(e)}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        解析HTML
        :param html: HTML字符串
        :return: BeautifulSoup对象
        """
        return BeautifulSoup(html, 'lxml')
    
    def extract_text(self, element, default: str = '') -> str:
        """
        提取文本内容
        :param element: BeautifulSoup元素
        :param default: 默认值
        :return: 文本内容
        """
        if element:
            return element.get_text(strip=True)
        return default
    
    def sleep(self, seconds: float = 1.0):
        """
        休眠
        :param seconds: 休眠秒数
        """
        time.sleep(seconds)
    
    def crawl(self) -> List[Dict]:
        """
        爬取数据（子类需实现）
        :return: 数据列表
        """
        raise NotImplementedError("子类必须实现crawl方法")

