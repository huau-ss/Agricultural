"""
决策辅助模块 - Django Admin配置
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import ProfitSimulation, DecisionAdvice


@admin.register(ProfitSimulation)
class ProfitSimulationAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'region', 'cost_info', 'revenue_info', 'profit_display', 'profit_rate_display', 'simulation_date']
    list_filter = ['product_name', 'region', 'simulation_date', 'created_at']
    search_fields = ['product_name', 'region']
    readonly_fields = ['created_at']
    list_per_page = 30
    date_hierarchy = 'simulation_date'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('product_name', 'region', 'simulation_date')
        }),
        ('成本信息', {
            'fields': ('purchase_price', 'quantity', 'transport_cost', 'storage_cost', 'other_cost', 'total_cost')
        }),
        ('收入信息', {
            'fields': ('sale_price', 'total_revenue')
        }),
        ('利润信息', {
            'fields': ('profit', 'profit_rate')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def cost_info(self, obj):
        return format_html(
            '采购: ¥{}<br/>'
            '运输: ¥{}<br/>'
            '仓储: ¥{}<br/>'
            '其他: ¥{}<br/>'
            '<strong>总计: ¥{}</strong>',
            obj.purchase_price,
            obj.transport_cost,
            obj.storage_cost,
            obj.other_cost,
            obj.total_cost
        )
    cost_info.short_description = '成本信息'
    
    def revenue_info(self, obj):
        return format_html(
            '售价: ¥{}<br/>'
            '数量: {}<br/>'
            '<strong>总计: ¥{}</strong>',
            obj.sale_price,
            obj.quantity,
            obj.total_revenue
        )
    revenue_info.short_description = '收入信息'
    
    def profit_display(self, obj):
        color = 'green' if obj.profit >= 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 14px;">¥{}</span>',
            color,
            obj.profit
        )
    profit_display.short_description = '利润'
    
    def profit_rate_display(self, obj):
        color = 'green' if obj.profit_rate >= 10 else 'orange' if obj.profit_rate >= 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.2f}%</span>',
            color,
            obj.profit_rate
        )
    profit_rate_display.short_description = '利润率'


@admin.register(DecisionAdvice)
class DecisionAdviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'region', 'advice_type', 'confidence_display', 'factors_list', 'created_at']
    list_filter = ['advice_type', 'product_name', 'region', 'created_at']
    search_fields = ['product_name', 'region', 'advice_content']
    readonly_fields = ['created_at']
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('product_name', 'region', 'advice_type')
        }),
        ('建议内容', {
            'fields': ('advice_content', 'confidence', 'factors')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def confidence_display(self, obj):
        color = 'green' if obj.confidence >= 0.8 else 'orange' if obj.confidence >= 0.6 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.0%}</span>',
            color,
            obj.confidence
        )
    confidence_display.short_description = '置信度'
    
    def factors_list(self, obj):
        if obj.factors:
            factors = obj.factors if isinstance(obj.factors, list) else []
            return ', '.join(factors[:3]) + ('...' if len(factors) > 3 else '')
        return '-'
    factors_list.short_description = '影响因素'

