"""
数据标准化工具
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler


class DataStandardizer:
    """数据标准化类"""
    
    def __init__(self, method='minmax'):
        """
        初始化标准化器
        :param method: 标准化方法 'minmax' 或 'standard'
        """
        self.method = method
        self.scaler = MinMaxScaler() if method == 'minmax' else StandardScaler()
        self.fitted = False
    
    def fit_transform(self, data):
        """
        拟合并转换数据
        :param data: 输入数据（numpy array 或 pandas DataFrame）
        :return: 标准化后的数据
        """
        if isinstance(data, pd.DataFrame):
            data = data.values
        
        scaled_data = self.scaler.fit_transform(data)
        self.fitted = True
        return scaled_data
    
    def transform(self, data):
        """
        转换数据（需要先fit）
        :param data: 输入数据
        :return: 标准化后的数据
        """
        if not self.fitted:
            raise ValueError("Scaler must be fitted before transform")
        
        if isinstance(data, pd.DataFrame):
            data = data.values
        
        return self.scaler.transform(data)
    
    def inverse_transform(self, data):
        """
        逆转换
        :param data: 标准化后的数据
        :return: 原始尺度的数据
        """
        if not self.fitted:
            raise ValueError("Scaler must be fitted before inverse_transform")
        
        return self.scaler.inverse_transform(data)
    
    def standardize(self, data: dict) -> dict:
        """
        标准化数据字典（清洗和规范化）
        :param data: 原始数据字典
        :return: 标准化后的数据字典
        """
        standardized = {}
        
        # 产品名称标准化
        product_name = data.get('product_name', '').strip()
        standardized['product_name'] = product_name
        
        # 产品类别标准化
        product_category = data.get('product_category', '').strip()
        standardized['product_category'] = product_category
        
        # 价格标准化
        price = data.get('price', 0)
        if isinstance(price, str):
            price = price.replace('¥', '').replace('元', '').strip()
            try:
                price = float(price)
            except:
                price = 0.0
        standardized['price'] = max(0, float(price))
        
        # 单位标准化
        unit = data.get('unit', '元/斤').strip()
        standardized['unit'] = unit if unit else '元/斤'
        
        # 市场名称标准化
        market_name = data.get('market_name', '').strip()
        standardized['market_name'] = market_name
        
        # 地区标准化
        region = data.get('region', '').strip()
        standardized['region'] = region
        
        # 日期标准化
        date = data.get('date')
        if isinstance(date, str):
            try:
                date = pd.to_datetime(date).date()
            except:
                from datetime import date as dt_date
                date = dt_date.today()
        standardized['date'] = date
        
        return standardized
    
    def calculate_quality_score(self, data: dict) -> float:
        """
        计算数据质量评分
        :param data: 数据字典
        :return: 质量评分 (0-1)
        """
        score = 1.0
        
        # 检查必填字段
        required_fields = ['product_name', 'price', 'date']
        for field in required_fields:
            if not data.get(field):
                score -= 0.3
        
        # 检查价格合理性
        price = data.get('price', 0)
        if price <= 0 or price > 10000:  # 假设价格范围
            score -= 0.2
        
        # 检查日期合理性
        from datetime import date, timedelta
        date_value = data.get('date')
        if date_value:
            if date_value > date.today():
                score -= 0.2
            elif date_value < date.today() - timedelta(days=365):
                score -= 0.1
        
        return max(0.0, min(1.0, score))

