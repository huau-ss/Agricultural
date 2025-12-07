"""
价格预测模块 - 数据模型
"""
from django.db import models


class ForecastModel(models.Model):
    """预测模型配置"""
    model_name = models.CharField(max_length=100, unique=True, verbose_name='模型名称')
    model_type = models.CharField(
        max_length=50,
        choices=[
            ('ARIMA', 'ARIMA模型'),
            ('LSTM', 'LSTM神经网络'),
            ('Linear', '线性回归'),
        ],
        verbose_name='模型类型'
    )
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    region = models.CharField(max_length=50, verbose_name='地区')
    parameters = models.JSONField(default=dict, verbose_name='模型参数')
    accuracy_metrics = models.JSONField(default=dict, verbose_name='准确度指标')
    model_file_path = models.CharField(max_length=255, blank=True, verbose_name='模型文件路径')
    status = models.CharField(
        max_length=20,
        choices=[
            ('training', '训练中'),
            ('ready', '就绪'),
            ('failed', '训练失败'),
        ],
        default='training',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    trained_at = models.DateTimeField(null=True, blank=True, verbose_name='训练时间')
    
    class Meta:
        db_table = 'forecast_model'
        verbose_name = '预测模型'
        verbose_name_plural = '预测模型'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.model_name} - {self.model_type}"


class ForecastResult(models.Model):
    """预测结果"""
    model = models.ForeignKey(ForecastModel, on_delete=models.CASCADE, verbose_name='预测模型')
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    region = models.CharField(max_length=50, verbose_name='地区')
    forecast_date = models.DateField(verbose_name='预测日期')
    forecast_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='预测价格')
    confidence_interval_lower = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        verbose_name='置信区间下限'
    )
    confidence_interval_upper = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        verbose_name='置信区间上限'
    )
    actual_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='实际价格'
    )
    error = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='预测误差'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'forecast_result'
        verbose_name = '预测结果'
        verbose_name_plural = '预测结果'
        ordering = ['-forecast_date', 'product_name']
        indexes = [
            models.Index(fields=['product_name', 'forecast_date']),
            models.Index(fields=['region', 'forecast_date']),
        ]
    
    def __str__(self):
        return f"{self.product_name} - {self.forecast_date} - {self.forecast_price}"


class TrainingHistory(models.Model):
    """训练历史记录"""
    model = models.ForeignKey(ForecastModel, on_delete=models.CASCADE, verbose_name='预测模型')
    training_data_start = models.DateField(verbose_name='训练数据起始日期')
    training_data_end = models.DateField(verbose_name='训练数据结束日期')
    data_count = models.IntegerField(verbose_name='数据量')
    training_duration = models.FloatField(null=True, verbose_name='训练时长(秒)')
    accuracy_metrics = models.JSONField(default=dict, verbose_name='准确度指标')
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', '成功'),
            ('failed', '失败'),
        ],
        verbose_name='状态'
    )
    error_message = models.TextField(blank=True, verbose_name='错误信息')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='训练时间')
    
    class Meta:
        db_table = 'training_history'
        verbose_name = '训练历史'
        verbose_name_plural = '训练历史'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.model.model_name} - {self.created_at}"

