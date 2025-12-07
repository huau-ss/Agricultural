"""
线性回归时间序列预测模型
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')


class LinearPredictor:
    """线性回归预测器"""
    
    def __init__(self, degree=1, use_trend=True, use_seasonal=False):
        """
        初始化线性回归预测器
        :param degree: 多项式阶数（1为线性，2为二次，以此类推）
        :param use_trend: 是否使用趋势特征
        :param use_seasonal: 是否使用季节性特征
        """
        self.degree = degree
        self.use_trend = use_trend
        self.use_seasonal = use_seasonal
        self.model = None
        self.poly_features = None
        self.is_fitted = False
    
    def create_features(self, ts):
        """
        创建特征
        :param ts: 时间序列数据（pandas Series，索引为日期）
        :return: 特征矩阵
        """
        features = []
        
        # 时间索引特征
        if isinstance(ts.index, pd.DatetimeIndex):
            dates = ts.index
            if self.use_trend:
                # 趋势特征（时间序号）
                trend = np.arange(len(ts))
                features.append(trend)
            
            if self.use_seasonal:
                # 季节性特征
                features.append(dates.dayofweek)  # 星期
                features.append(dates.dayofyear)  # 一年中的第几天
                features.append(dates.month)  # 月份
        
        # 历史值特征
        values = ts.values
        features.append(values)
        
        # 组合特征
        X = np.column_stack(features) if len(features) > 1 else features[0].reshape(-1, 1)
        
        # 多项式特征
        if self.degree > 1:
            self.poly_features = PolynomialFeatures(degree=self.degree, include_bias=False)
            X = self.poly_features.fit_transform(X)
        
        return X
    
    def train(self, ts):
        """
        训练线性回归模型
        :param ts: 时间序列数据（pandas Series）
        :return: 训练好的模型
        """
        X = self.create_features(ts)
        y = ts.values
        
        self.model = LinearRegression()
        self.model.fit(X, y)
        self.is_fitted = True
        
        return self.model
    
    def predict(self, steps=7, last_ts=None):
        """
        预测未来值
        :param steps: 预测步数
        :param last_ts: 最后的时间序列（用于生成未来特征）
        :return: 预测值数组
        """
        if not self.is_fitted or self.model is None:
            raise ValueError("模型未训练，请先调用train方法")
        
        if last_ts is None:
            raise ValueError("需要提供last_ts参数")
        
        predictions = []
        current_ts = last_ts.copy()
        
        # 获取最后的时间索引
        if isinstance(current_ts.index, pd.DatetimeIndex):
            last_date = current_ts.index[-1]
            future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=steps, freq='D')
        else:
            future_dates = None
        
        for i in range(steps):
            # 创建特征
            X = self.create_features(current_ts)
            
            # 预测
            pred = self.model.predict(X[-1:].reshape(1, -1))[0]
            predictions.append(pred)
            
            # 更新序列（添加预测值）
            if future_dates is not None:
                new_ts = pd.Series([pred], index=[future_dates[i]])
            else:
                new_ts = pd.Series([pred])
            current_ts = pd.concat([current_ts, new_ts])
        
        return np.array(predictions)
    
    def evaluate(self, test_ts, train_ts=None):
        """
        评估模型性能
        :param test_ts: 测试集时间序列
        :param train_ts: 训练集时间序列（用于特征生成）
        :return: 评估指标字典
        """
        if not self.is_fitted or self.model is None:
            raise ValueError("模型未训练，请先调用train方法")
        
        if train_ts is None:
            raise ValueError("需要提供train_ts参数用于生成特征")
        
        # 准备测试数据
        full_ts = pd.concat([train_ts, test_ts])
        X_test = self.create_features(full_ts)
        X_test = X_test[-len(test_ts):]
        y_test = test_ts.values
        
        # 预测
        predictions = self.model.predict(X_test)
        
        # 计算评估指标
        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100
        
        return {
            'mae': float(mae),
            'mse': float(mse),
            'rmse': float(rmse),
            'mape': float(mape),
        }
    
    def get_model_info(self):
        """获取模型信息"""
        if self.model is None:
            return None
        
        return {
            'degree': self.degree,
            'use_trend': self.use_trend,
            'use_seasonal': self.use_seasonal,
            'coefficients': self.model.coef_.tolist() if hasattr(self.model, 'coef_') else None,
            'intercept': float(self.model.intercept_) if hasattr(self.model, 'intercept_') else None,
        }

