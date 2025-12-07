"""
市场行情模块 - 数据模型
"""
from django.db import models
from apps.data_etl.models import CleanedData


class MarketPrice(models.Model):
    """市场价格数据（从清洗数据同步）"""
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    product_category = models.CharField(max_length=50, verbose_name='农产品类别')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    unit = models.CharField(max_length=20, default='元/斤', verbose_name='单位')
    market_name = models.CharField(max_length=100, verbose_name='市场名称')
    region = models.CharField(max_length=50, verbose_name='地区')
    date = models.DateField(verbose_name='日期')
    price_change = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='价格变化'
    )
    price_change_rate = models.FloatField(
        null=True,
        blank=True,
        verbose_name='价格变化率(%)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'market_price'
        verbose_name = '市场价格'
        verbose_name_plural = '市场价格'
        ordering = ['-date', 'product_name']
        indexes = [
            models.Index(fields=['product_name', 'date']),
            models.Index(fields=['region', 'date']),
            models.Index(fields=['date']),
        ]
        unique_together = [['product_name', 'market_name', 'date']]
    
    def __str__(self):
        return f"{self.product_name} - {self.market_name} - {self.date}"


class MarketStatistics(models.Model):
    """市场统计数据（日/周/月汇总）"""
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    product_category = models.CharField(max_length=50, verbose_name='农产品类别')
    region = models.CharField(max_length=50, verbose_name='地区')
    stat_date = models.DateField(verbose_name='统计日期')
    stat_type = models.CharField(
        max_length=20,
        choices=[
            ('daily', '日统计'),
            ('weekly', '周统计'),
            ('monthly', '月统计'),
        ],
        verbose_name='统计类型'
    )
    avg_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='平均价格')
    max_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='最高价格')
    min_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='最低价格')
    price_std = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='价格标准差')
    volume = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='交易量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'market_statistics'
        verbose_name = '市场统计'
        verbose_name_plural = '市场统计'
        ordering = ['-stat_date', 'product_name']
        indexes = [
            models.Index(fields=['product_name', 'stat_date']),
            models.Index(fields=['region', 'stat_date']),
        ]
        unique_together = [['product_name', 'region', 'stat_date', 'stat_type']]
    
    def __str__(self):
        return f"{self.product_name} - {self.stat_type} - {self.stat_date}"

