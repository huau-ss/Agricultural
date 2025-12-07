"""
LSTM神经网络时间序列预测模型
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import warnings
warnings.filterwarnings('ignore')


class LSTMPredictor:
    """LSTM预测器"""
    
    def __init__(self, sequence_length=30, units=50, epochs=100, batch_size=32):
        """
        初始化LSTM预测器
        :param sequence_length: 输入序列长度
        :param units: LSTM单元数
        :param epochs: 训练轮数
        :param batch_size: 批次大小
        """
        self.sequence_length = sequence_length
        self.units = units
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.is_fitted = False
    
    def create_sequences(self, data):
        """
        创建时间序列数据
        :param data: 一维数组
        :return: (X, y)
        """
        X, y = [], []
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:i + self.sequence_length])
            y.append(data[i + self.sequence_length])
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape):
        """
        构建LSTM模型
        :param input_shape: 输入形状
        :return: 模型对象
        """
        model = Sequential([
            LSTM(self.units, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(self.units, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return model
    
    def train(self, ts, validation_split=0.2):
        """
        训练LSTM模型
        :param ts: 时间序列数据（pandas Series）
        :param validation_split: 验证集比例
        :return: 训练历史
        """
        # 数据预处理
        values = ts.values.reshape(-1, 1)
        scaled_values = self.scaler.fit_transform(values)
        
        # 创建序列
        X, y = self.create_sequences(scaled_values.flatten())
        
        # 划分训练集和验证集
        split_idx = int(len(X) * (1 - validation_split))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # 重塑数据为LSTM输入格式
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))
        
        # 构建和训练模型
        self.model = self.build_model((X_train.shape[1], 1))
        history = self.model.fit(
            X_train, y_train,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_data=(X_val, y_val),
            verbose=0
        )
        
        self.is_fitted = True
        return history
    
    def predict(self, steps=7, last_sequence=None):
        """
        预测未来值
        :param steps: 预测步数
        :param last_sequence: 最后的序列（用于预测）
        :return: 预测值数组
        """
        if not self.is_fitted or self.model is None:
            raise ValueError("模型未训练，请先调用train方法")
        
        if last_sequence is None:
            # 使用训练数据的最后sequence_length个值
            raise ValueError("需要提供last_sequence参数")
        
        # 标准化
        last_sequence_scaled = self.scaler.transform(last_sequence.reshape(-1, 1)).flatten()
        
        predictions = []
        current_sequence = last_sequence_scaled[-self.sequence_length:].copy()
        
        for _ in range(steps):
            # 预测下一个值
            X_input = current_sequence.reshape((1, self.sequence_length, 1))
            next_pred = self.model.predict(X_input, verbose=0)[0, 0]
            predictions.append(next_pred)
            
            # 更新序列
            current_sequence = np.append(current_sequence[1:], next_pred)
        
        # 反标准化
        predictions = np.array(predictions).reshape(-1, 1)
        predictions = self.scaler.inverse_transform(predictions).flatten()
        
        return predictions
    
    def evaluate(self, test_ts):
        """
        评估模型性能
        :param test_ts: 测试集时间序列
        :return: 评估指标字典
        """
        if not self.is_fitted or self.model is None:
            raise ValueError("模型未训练，请先调用train方法")
        
        # 准备测试数据
        values = test_ts.values.reshape(-1, 1)
        scaled_values = self.scaler.transform(values)
        
        # 创建序列
        X_test, y_test = self.create_sequences(scaled_values.flatten())
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
        
        # 预测
        predictions_scaled = self.model.predict(X_test, verbose=0)
        predictions = self.scaler.inverse_transform(predictions_scaled)
        y_test_actual = self.scaler.inverse_transform(y_test.reshape(-1, 1))
        
        # 计算评估指标
        mae = np.mean(np.abs(predictions - y_test_actual))
        mse = np.mean((predictions - y_test_actual) ** 2)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((y_test_actual - predictions) / y_test_actual)) * 100
        
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
            'sequence_length': self.sequence_length,
            'units': self.units,
            'epochs': self.epochs,
            'batch_size': self.batch_size,
            'total_params': self.model.count_params(),
        }

