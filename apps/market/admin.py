"""
市场行情模块 - Django Admin配置
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import MarketPrice, MarketStatistics


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'product_category', 'region', 'market_name', 'price_display', 'unit', 'date', 'change_rate_display', 'created_at']
    list_filter = ['product_category', 'region', 'date', 'created_at']
    search_fields = ['product_name', 'market_name', 'region']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']
    list_per_page = 50
    
    fieldsets = (
        ('产品信息', {
            'fields': ('product_name', 'product_category')
        }),
        ('价格信息', {
            'fields': ('price', 'unit', 'price_change', 'price_change_rate')
        }),
        ('市场信息', {
            'fields': ('market_name', 'region', 'date')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        return format_html('<strong style="color: #409EFF;">¥{}</strong>', obj.price)
    price_display.short_description = '价格'
    
    def change_rate_display(self, obj):
        if obj.price_change_rate is None:
            return '-'
        color = 'red' if obj.price_change_rate >= 0 else 'green'
        symbol = '+' if obj.price_change_rate >= 0 else ''
        return format_html(
            '<span style="color: {};">{}{:.2f}%</span>',
            color,
            symbol,
            obj.price_change_rate
        )
    change_rate_display.short_description = '变化率'


@admin.register(MarketStatistics)
class MarketStatisticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'product_category', 'region', 'stat_type', 'stat_date', 'price_range', 'avg_price', 'volume']
    list_filter = ['product_category', 'region', 'stat_type', 'stat_date']
    search_fields = ['product_name', 'region']
    date_hierarchy = 'stat_date'
    list_per_page = 50
    
    def price_range(self, obj):
        return format_html(
            '最低: <span style="color: #67C23A;">¥{}</span><br/>'
            '最高: <span style="color: #F56C6C;">¥{}</span><br/>'
            '平均: <span style="color: #409EFF; font-weight: bold;">¥{}</span>',
            obj.min_price,
            obj.max_price,
            obj.avg_price
        )
    price_range.short_description = '价格区间'

