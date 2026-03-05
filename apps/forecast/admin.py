"""
价格预测模块 - Django Admin配置
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import ForecastModel, ForecastResult, TrainingHistory


@admin.register(ForecastModel)
class ForecastModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'model_name', 'model_type_display', 'product_name', 'region', 'status_display', 'accuracy_display', 'trained_at', 'created_at']
    list_filter = ['model_type', 'status', 'product_name', 'region', 'created_at']
    search_fields = ['model_name', 'product_name', 'region']
    readonly_fields = ['created_at', 'updated_at', 'trained_at']
    list_per_page = 30
    
    fieldsets = (
        ('模型信息', {
            'fields': ('model_name', 'model_type', 'product_name', 'region')
        }),
        ('模型配置', {
            'fields': ('parameters', 'status'),
            'classes': ('collapse',)
        }),
        ('训练信息', {
            'fields': ('trained_at', 'accuracy', 'training_data_count')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def model_type_display(self, obj):
        types = {
            'arima': 'ARIMA模型',
            'lstm': 'LSTM神经网络',
            'linear': '线性回归'
        }
        return types.get(obj.model_type, obj.model_type)
    model_type_display.short_description = '模型类型'
    
    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'training': 'blue',
            'trained': 'green',
            'failed': 'red'
        }
        color = colors.get(obj.status, 'black')
        status_text = {
            'pending': '待训练',
            'training': '训练中',
            'trained': '已训练',
            'failed': '训练失败'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            status_text.get(obj.status, obj.status)
        )
    status_display.short_description = '状态'
    
    def accuracy_display(self, obj):
        if obj.accuracy:
            color = 'green' if obj.accuracy >= 80 else 'orange' if obj.accuracy >= 60 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{:.2f}%</span>',
                color,
                obj.accuracy
            )
        return '-'
    accuracy_display.short_description = '准确度'


@admin.register(ForecastResult)
class ForecastResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'region', 'forecast_date', 'price_comparison', 'error_display', 'created_at']
    list_filter = ['product_name', 'region', 'forecast_date', 'created_at']
    search_fields = ['product_name', 'region']
    date_hierarchy = 'forecast_date'
    readonly_fields = ['created_at']
    list_per_page = 50
    
    def price_comparison(self, obj):
        if obj.actual_price:
            diff = float(obj.forecast_price) - float(obj.actual_price)
            color = 'red' if diff > 0 else 'green'
            symbol = '+' if diff > 0 else ''
            return format_html(
                '预测: <strong>¥{}</strong><br/>'
                '实际: <strong>¥{}</strong><br/>'
                '误差: <span style="color: {};">{}{:.2f}</span>',
                obj.forecast_price,
                obj.actual_price,
                color,
                symbol,
                diff
            )
        return format_html('预测: <strong>¥{}</strong>', obj.forecast_price)
    price_comparison.short_description = '价格对比'
    
    def error_display(self, obj):
        if obj.error:
            color = 'red' if abs(float(obj.error)) > 1 else 'orange'
            return format_html(
                '<span style="color: {};">{:.2f}</span>',
                color,
                float(obj.error)
            )
        return '-'
    error_display.short_description = '误差'


@admin.register(TrainingHistory)
class TrainingHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'data_range', 'data_count', 'status_display', 'duration', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['model__model_name']
    readonly_fields = ['created_at']
    list_per_page = 30
    
    def data_range(self, obj):
        return format_html(
            '{} 至 {}',
            obj.training_data_start,
            obj.training_data_end
        )
    data_range.short_description = '数据范围'
    
    def status_display(self, obj):
        colors = {
            'running': 'blue',
            'success': 'green',
            'failed': 'red'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = '状态'
    
    def duration(self, obj):
        if obj.training_duration:
            seconds = obj.training_duration
            if seconds < 60:
                return f'{int(seconds)}秒'
            elif seconds < 3600:
                return f'{int(seconds/60)}分钟'
            else:
                return f'{int(seconds/3600)}小时{int((seconds%3600)/60)}分钟'
        return '-'
    duration.short_description = '训练时长'

