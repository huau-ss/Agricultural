"""
供需对接模块 - Django Admin配置
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import SupplyInfo, DemandInfo, TradeMatch


@admin.register(SupplyInfo)
class SupplyInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'product_category', 'region', 'quantity', 'unit', 'price', 'contact_name', 'contact_phone', 'status', 'created_at']
    list_filter = ['product_category', 'region', 'status', 'created_at']
    search_fields = ['product_name', 'region', 'contact_name', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('product_name', 'product_category', 'region')
        }),
        ('供应信息', {
            'fields': ('quantity', 'unit', 'price')
        }),
        ('联系信息', {
            'fields': ('contact_name', 'contact_phone', 'description')
        }),
        ('状态信息', {
            'fields': ('status', 'expire_at')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DemandInfo)
class DemandInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'product_category', 'region', 'quantity', 'unit', 'max_price', 'contact_name', 'contact_phone', 'status', 'created_at']
    list_filter = ['product_category', 'region', 'status', 'created_at']
    search_fields = ['product_name', 'region', 'contact_name', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('product_name', 'product_category', 'region')
        }),
        ('需求信息', {
            'fields': ('quantity', 'unit', 'max_price')
        }),
        ('联系信息', {
            'fields': ('contact_name', 'contact_phone', 'description')
        }),
        ('状态信息', {
            'fields': ('status', 'expire_at')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TradeMatch)
class TradeMatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'supply_info', 'demand_info', 'match_score_display', 'status', 'created_at', 'confirmed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['supply__product_name', 'demand__product_name']
    readonly_fields = ['created_at', 'confirmed_at']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    def supply_info(self, obj):
        return format_html(
            '<strong>{}</strong><br/>{} {}<br/>¥{}/{}',
            obj.supply.product_name,
            obj.supply.quantity,
            obj.supply.unit,
            obj.supply.price,
            obj.supply.unit
        )
    supply_info.short_description = '供应信息'
    
    def demand_info(self, obj):
        return format_html(
            '<strong>{}</strong><br/>{} {}<br/>最高¥{}/{}',
            obj.demand.product_name,
            obj.demand.quantity,
            obj.demand.unit,
            obj.demand.max_price or '不限',
            obj.demand.unit
        )
    demand_info.short_description = '需求信息'
    
    def match_score_display(self, obj):
        color = 'green' if obj.match_score >= 80 else 'orange' if obj.match_score >= 60 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color,
            obj.match_score
        )
    match_score_display.short_description = '匹配度'

