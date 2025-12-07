"""
数据采集与清洗模块 - 数据模型
"""
from django.db import models
from django.utils import timezone


class DataSource(models.Model):
    """数据源配置"""
    name = models.CharField(max_length=100, verbose_name='数据源名称')
    url = models.URLField(verbose_name='数据源URL')
    source_type = models.CharField(
        max_length=50,
        choices=[
            ('web', '网页爬虫'),
            ('api', 'API接口'),
            ('file', '文件导入'),
        ],
        default='web',
        verbose_name='数据源类型'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', '启用'),
            ('inactive', '禁用'),
        ],
        default='active',
        verbose_name='状态'
    )
    config = models.JSONField(default=dict, verbose_name='配置信息', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'data_source'
        verbose_name = '数据源'
        verbose_name_plural = '数据源'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class RawData(models.Model):
    """原始数据"""
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, verbose_name='数据源')
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    product_category = models.CharField(max_length=50, verbose_name='农产品类别')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    unit = models.CharField(max_length=20, default='元/斤', verbose_name='单位')
    market_name = models.CharField(max_length=100, verbose_name='市场名称')
    region = models.CharField(max_length=50, verbose_name='地区')
    date = models.DateField(verbose_name='日期')
    raw_content = models.TextField(verbose_name='原始内容', blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待清洗'),
            ('cleaned', '已清洗'),
            ('error', '清洗失败'),
        ],
        default='pending',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='采集时间')
    
    class Meta:
        db_table = 'raw_data'
        verbose_name = '原始数据'
        verbose_name_plural = '原始数据'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['product_name', 'date']),
            models.Index(fields=['region', 'date']),
        ]
    
    def __str__(self):
        return f"{self.product_name} - {self.market_name} - {self.date}"


class CleanedData(models.Model):
    """清洗后的数据"""
    raw_data = models.OneToOneField(RawData, on_delete=models.CASCADE, verbose_name='原始数据')
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    product_category = models.CharField(max_length=50, verbose_name='农产品类别')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    unit = models.CharField(max_length=20, default='元/斤', verbose_name='单位')
    market_name = models.CharField(max_length=100, verbose_name='市场名称')
    region = models.CharField(max_length=50, verbose_name='地区')
    date = models.DateField(verbose_name='日期')
    quality_score = models.FloatField(default=1.0, verbose_name='数据质量评分')
    cleaned_at = models.DateTimeField(auto_now_add=True, verbose_name='清洗时间')
    
    class Meta:
        db_table = 'cleaned_data'
        verbose_name = '清洗数据'
        verbose_name_plural = '清洗数据'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['product_name', 'date']),
            models.Index(fields=['region', 'date']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.product_name} - {self.date}"


class ETLTask(models.Model):
    """ETL任务记录"""
    task_name = models.CharField(max_length=100, verbose_name='任务名称')
    source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, verbose_name='数据源')
    status = models.CharField(
        max_length=20,
        choices=[
            ('running', '运行中'),
            ('success', '成功'),
            ('failed', '失败'),
        ],
        default='running',
        verbose_name='状态'
    )
    total_count = models.IntegerField(default=0, verbose_name='总记录数')
    success_count = models.IntegerField(default=0, verbose_name='成功数')
    failed_count = models.IntegerField(default=0, verbose_name='失败数')
    error_message = models.TextField(blank=True, verbose_name='错误信息')
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    
    class Meta:
        db_table = 'etl_task'
        verbose_name = 'ETL任务'
        verbose_name_plural = 'ETL任务'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.task_name} - {self.status}"

