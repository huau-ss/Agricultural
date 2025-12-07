from django.contrib import admin
from .models import DataSource, RawData, CleanedData, ETLTask


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'status', 'created_at']
    list_filter = ['source_type', 'status']
    search_fields = ['name', 'url']


@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'market_name', 'price', 'date', 'status', 'created_at']
    list_filter = ['status', 'product_category', 'region', 'date']
    search_fields = ['product_name', 'market_name']
    date_hierarchy = 'date'


@admin.register(CleanedData)
class CleanedDataAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'market_name', 'price', 'date', 'quality_score', 'cleaned_at']
    list_filter = ['product_category', 'region', 'date']
    search_fields = ['product_name', 'market_name']
    date_hierarchy = 'date'


@admin.register(ETLTask)
class ETLTaskAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'source', 'status', 'total_count', 'success_count', 'failed_count', 'started_at']
    list_filter = ['status', 'started_at']
    search_fields = ['task_name']
    readonly_fields = ['started_at', 'finished_at']

