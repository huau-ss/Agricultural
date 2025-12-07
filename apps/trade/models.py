"""
供需对接模块 - 数据模型
"""
from django.db import models


class SupplyInfo(models.Model):
    """供应信息"""
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    product_category = models.CharField(max_length=50, verbose_name='农产品类别')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='供应数量')
    unit = models.CharField(max_length=20, default='斤', verbose_name='单位')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    region = models.CharField(max_length=50, verbose_name='地区')
    contact_name = models.CharField(max_length=50, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    description = models.TextField(blank=True, verbose_name='描述')
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', '有效'),
            ('completed', '已完成'),
            ('cancelled', '已取消'),
        ],
        default='active',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    expire_at = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    
    class Meta:
        db_table = 'supply_info'
        verbose_name = '供应信息'
        verbose_name_plural = '供应信息'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product_name', 'status']),
            models.Index(fields=['region', 'status']),
        ]
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity}{self.unit} - {self.region}"


class DemandInfo(models.Model):
    """需求信息"""
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    product_category = models.CharField(max_length=50, verbose_name='农产品类别')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='需求数量')
    unit = models.CharField(max_length=20, default='斤', verbose_name='单位')
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='最高价格')
    region = models.CharField(max_length=50, verbose_name='地区')
    contact_name = models.CharField(max_length=50, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    description = models.TextField(blank=True, verbose_name='描述')
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', '有效'),
            ('completed', '已完成'),
            ('cancelled', '已取消'),
        ],
        default='active',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    expire_at = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    
    class Meta:
        db_table = 'demand_info'
        verbose_name = '需求信息'
        verbose_name_plural = '需求信息'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product_name', 'status']),
            models.Index(fields=['region', 'status']),
        ]
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity}{self.unit} - {self.region}"


class TradeMatch(models.Model):
    """交易匹配记录"""
    supply = models.ForeignKey(SupplyInfo, on_delete=models.CASCADE, verbose_name='供应信息')
    demand = models.ForeignKey(DemandInfo, on_delete=models.CASCADE, verbose_name='需求信息')
    match_score = models.FloatField(verbose_name='匹配度')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待确认'),
            ('confirmed', '已确认'),
            ('completed', '已完成'),
            ('cancelled', '已取消'),
        ],
        default='pending',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='匹配时间')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='确认时间')
    
    class Meta:
        db_table = 'trade_match'
        verbose_name = '交易匹配'
        verbose_name_plural = '交易匹配'
        ordering = ['-match_score', '-created_at']
    
    def __str__(self):
        return f"{self.supply.product_name} - 匹配度: {self.match_score}"

