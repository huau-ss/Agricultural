"""
数据采集爬虫模块
"""
from .agricultural_price_spider import AgriculturalPriceSpider
from .pfsc_spider import PFSCSpider

__all__ = ['AgriculturalPriceSpider', 'PFSCSpider']

