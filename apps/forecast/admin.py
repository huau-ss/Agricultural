"""
价格预测模块 - Django Admin配置
"""
from django.contrib import admin
from .models import ForecastModel, ForecastResult, TrainingHistory


@admin.register(ForecastModel)
class ForecastModelAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'model_type', 'product_name', 'region', 'status', 'created_at', 'trained_at']
    list_filter = ['model_type', 'status', 'product_name', 'region']
    search_fields = ['model_name', 'product_name', 'region']
    readonly_fields = ['created_at', 'updated_at', 'trained_at']


@admin.register(ForecastResult)
class ForecastResultAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'region', 'forecast_date', 'forecast_price', 'actual_price', 'error', 'created_at']
    list_filter = ['product_name', 'region', 'forecast_date']
    search_fields = ['product_name', 'region']
    date_hierarchy = 'forecast_date'
    readonly_fields = ['created_at']


@admin.register(TrainingHistory)
class TrainingHistoryAdmin(admin.ModelAdmin):
    list_display = ['model', 'training_data_start', 'training_data_end', 'data_count', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['model__model_name']
    readonly_fields = ['created_at']

