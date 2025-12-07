"""
决策辅助模块 - 数据模型
"""
from django.db import models
from decimal import Decimal


class ProfitSimulation(models.Model):
    """利润模拟"""
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    region = models.CharField(max_length=50, verbose_name='地区')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='采购价格')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='销售价格')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='数量')
    unit = models.CharField(max_length=20, default='斤', verbose_name='单位')
    transport_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='运输成本'
    )
    storage_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='仓储成本'
    )
    other_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='其他成本'
    )
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='总成本')
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='总收入')
    profit = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='利润')
    profit_rate = models.FloatField(verbose_name='利润率(%)')
    simulation_date = models.DateField(verbose_name='模拟日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'profit_simulation'
        verbose_name = '利润模拟'
        verbose_name_plural = '利润模拟'
        ordering = ['-simulation_date', '-created_at']
    
    def __str__(self):
        return f"{self.product_name} - {self.simulation_date} - 利润: {self.profit}"


class DecisionAdvice(models.Model):
    """决策建议"""
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    region = models.CharField(max_length=50, verbose_name='地区')
    advice_type = models.CharField(
        max_length=50,
        choices=[
            ('purchase', '采购建议'),
            ('sale', '销售建议'),
            ('storage', '仓储建议'),
            ('transport', '运输建议'),
        ],
        verbose_name='建议类型'
    )
    advice_content = models.TextField(verbose_name='建议内容')
    confidence = models.FloatField(default=0.0, verbose_name='置信度')
    factors = models.JSONField(default=list, verbose_name='影响因素')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'decision_advice'
        verbose_name = '决策建议'
        verbose_name_plural = '决策建议'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product_name} - {self.advice_type}"

