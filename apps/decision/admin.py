"""
决策辅助模块 - Django Admin配置
"""
from django.contrib import admin
from .models import ProfitSimulation, DecisionAdvice


@admin.register(ProfitSimulation)
class ProfitSimulationAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'region', 'purchase_price', 'sale_price', 'profit', 'profit_rate', 'simulation_date']
    list_filter = ['product_name', 'region', 'simulation_date']
    search_fields = ['product_name', 'region']
    readonly_fields = ['created_at']


@admin.register(DecisionAdvice)
class DecisionAdviceAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'region', 'advice_type', 'confidence', 'created_at']
    list_filter = ['advice_type', 'product_name', 'region']
    search_fields = ['product_name', 'region', 'advice_content']
    readonly_fields = ['created_at']

