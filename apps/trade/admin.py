"""
供需对接模块 - Django Admin配置
"""
from django.contrib import admin
from .models import SupplyInfo, DemandInfo, TradeMatch


@admin.register(SupplyInfo)
class SupplyInfoAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'region', 'quantity', 'price', 'contact_name', 'status', 'created_at']
    list_filter = ['product_category', 'region', 'status', 'created_at']
    search_fields = ['product_name', 'region', 'contact_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DemandInfo)
class DemandInfoAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'region', 'quantity', 'max_price', 'contact_name', 'status', 'created_at']
    list_filter = ['product_category', 'region', 'status', 'created_at']
    search_fields = ['product_name', 'region', 'contact_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TradeMatch)
class TradeMatchAdmin(admin.ModelAdmin):
    list_display = ['supply', 'demand', 'match_score', 'status', 'created_at', 'confirmed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['supply__product_name', 'demand__product_name']
    readonly_fields = ['created_at', 'confirmed_at']

