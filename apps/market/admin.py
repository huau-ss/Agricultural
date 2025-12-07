"""
市场行情模块 - Django Admin配置
"""
from django.contrib import admin
from .models import MarketPrice, MarketStatistics


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'region', 'market_name', 'price', 'date', 'price_change_rate', 'created_at']
    list_filter = ['product_category', 'region', 'date']
    search_fields = ['product_name', 'market_name', 'region']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']


@admin.register(MarketStatistics)
class MarketStatisticsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'region', 'stat_type', 'stat_date', 'avg_price', 'max_price', 'min_price']
    list_filter = ['product_category', 'region', 'stat_type', 'stat_date']
    search_fields = ['product_name', 'region']
    date_hierarchy = 'stat_date'

