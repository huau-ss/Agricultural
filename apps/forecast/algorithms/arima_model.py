"""
ARIMA时间序列预测模型
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings
warnings.filterwarnings('ignore')


class ARIMAPredictor:
    """ARIMA预测器"""
    
    def __init__(self, max_p=5, max_d=2, max_q=5, seasonal=True, seasonal_periods=12):
        """
        初始化ARIMA预测器
        :param max_p: 自回归项最大阶数
        :param max_d: 差分项最大阶数
        :param max_q: 移动平均项最大阶数
        :param seasonal: 是否使用季节性ARIMA
        :param seasonal_periods: 季节性周期
        """
        self.max_p = max_p
        self.max_d = max_d
        self.max_q = max_q
        self.seasonal = seasonal
        self.seasonal_periods = seasonal_periods
        self.model = None
        self.best_params = None
        self.fitted_model = None
    
    def check_stationarity(self, ts):
        """
        检查时间序列的平稳性
        :param ts: 时间序列数据
        :return: (is_stationary, adf_result)
        """
        adf_result = adfuller(ts.dropna())
        is_stationary = adf_result[1] <= 0.05
        return is_stationary, adf_result
    
    def find_best_params(self, ts):
        """
        寻找最佳ARIMA参数
        :param ts: 时间序列数据
        :return: 最佳参数 (p, d, q)
        """
        best_aic = np.inf
        best_params = (0, 0, 0)
        
        # 确定差分阶数d
        d = 0
        current_ts = ts.copy()
        
        for i in range(self.max_d + 1):
            is_stationary, _ = self.check_stationarity(current_ts)
            if is_stationary:
                d = i
                break
            if i < self.max_d:
                current_ts = current_ts.diff().dropna()
        
        # 网格搜索最佳p和q
        for p in range(self.max_p + 1):
            for q in range(self.max_q + 1):
                try:
                    if self.seasonal:
                        model = ARIMA(
                            ts,
                            order=(p, d, q),
                            seasonal_order=(p, d, q, self.seasonal_periods)
                        )
                    else:
                        model = ARIMA(ts, order=(p, d, q))
                    
                    fitted_model = model.fit()
                    aic = fitted_model.aic
                    
                    if aic < best_aic:
                        best_aic = aic
                        best_params = (p, d, q)
                        self.fitted_model = fitted_model
                except:
                    continue
        
        self.best_params = best_params
        return best_params
    
    def train(self, ts, auto_params=True):
        """
        训练ARIMA模型
        :param ts: 时间序列数据（pandas Series，索引为日期）
        :param auto_params: 是否自动寻找最佳参数
        :return: 训练好的模型
        """
        if auto_params:
            self.find_best_params(ts)
        else:
            # 使用默认参数
            p, d, q = 1, 1, 1
            self.best_params = (p, d, q)
        
        if self.fitted_model is None:
            if self.seasonal:
                self.model = ARIMA(
                    ts,
                    order=self.best_params,
                    seasonal_order=(*self.best_params, self.seasonal_periods)
                )
            else:
                self.model = ARIMA(ts, order=self.best_params)
            self.fitted_model = self.model.fit()
        
        return self.fitted_model
    
    def predict(self, steps=7, confidence_level=0.95):
        """
        预测未来值
        :param steps: 预测步数
        :param confidence_level: 置信水平
        :return: (预测值, 置信区间)
        """
        if self.fitted_model is None:
            raise ValueError("模型未训练，请先调用train方法")
        
        forecast = self.fitted_model.forecast(steps=steps)
        conf_int = self.fitted_model.get_forecast(steps=steps).conf_int(alpha=1-confidence_level)
        
        return forecast, conf_int
    
    def evaluate(self, test_ts):
        """
        评估模型性能
        :param test_ts: 测试集时间序列
        :return: 评估指标字典
        """
        if self.fitted_model is None:
            raise ValueError("模型未训练，请先调用train方法")
        
        predictions, _ = self.predict(steps=len(test_ts))
        
        # 计算评估指标
        mae = np.mean(np.abs(predictions - test_ts))
        mse = np.mean((predictions - test_ts) ** 2)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((test_ts - predictions) / test_ts)) * 100
        
        return {
            'mae': float(mae),
            'mse': float(mse),
            'rmse': float(rmse),
            'mape': float(mape),
            'best_params': self.best_params,
        }
    
    def get_model_info(self):
        """获取模型信息"""
        if self.fitted_model is None:
            return None
        
        return {
            'params': self.best_params,
            'aic': float(self.fitted_model.aic),
            'bic': float(self.fitted_model.bic),
            'summary': str(self.fitted_model.summary()),
        }

