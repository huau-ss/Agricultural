from django.contrib import admin
from django.utils.html import format_html
from .models import DataSource, RawData, CleanedData, ETLTask


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'source_type_display', 'status_display', 'url_short', 'created_at']
    list_filter = ['source_type', 'status', 'created_at']
    search_fields = ['name', 'url']
    list_per_page = 30
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'url', 'source_type', 'status')
        }),
        ('配置信息', {
            'fields': ('config',),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def source_type_display(self, obj):
        types = {
            'web': '网页爬虫',
            'api': 'API接口',
            'file': '文件导入'
        }
        return types.get(obj.source_type, obj.source_type)
    source_type_display.short_description = '数据源类型'
    
    def status_display(self, obj):
        if obj.status == 'active':
            return format_html('<span style="color: green;">✓ 启用</span>')
        return format_html('<span style="color: gray;">禁用</span>')
    status_display.short_description = '状态'
    
    def url_short(self, obj):
        if len(obj.url) > 50:
            return obj.url[:50] + '...'
        return obj.url
    url_short.short_description = 'URL'


@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'product_category', 'region', 'market_name', 'price_display', 'unit', 'date', 'status_display', 'created_at']
    list_filter = ['status', 'product_category', 'region', 'date', 'created_at']
    search_fields = ['product_name', 'market_name', 'region']
    date_hierarchy = 'date'
    list_per_page = 50
    readonly_fields = ['created_at', 'raw_content']
    
    def price_display(self, obj):
        return format_html('<strong style="color: #409EFF;">¥{}</strong>', obj.price)
    price_display.short_description = '价格'
    
    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'cleaned': 'green',
            'error': 'red'
        }
        color = colors.get(obj.status, 'black')
        status_text = {
            'pending': '待清洗',
            'cleaned': '已清洗',
            'error': '清洗失败'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            status_text.get(obj.status, obj.status)
        )
    status_display.short_description = '状态'


@admin.register(CleanedData)
class CleanedDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'product_category', 'region', 'market_name', 'price_display', 'unit', 'date', 'quality_score_display', 'cleaned_at']
    list_filter = ['product_category', 'region', 'date', 'cleaned_at']
    search_fields = ['product_name', 'market_name', 'region']
    date_hierarchy = 'date'
    list_per_page = 50
    readonly_fields = ['cleaned_at']
    
    def price_display(self, obj):
        return format_html('<strong style="color: #409EFF;">¥{}</strong>', obj.price)
    price_display.short_description = '价格'
    
    def quality_score_display(self, obj):
        color = 'green' if obj.quality_score >= 0.8 else 'orange' if obj.quality_score >= 0.6 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.2f}</span>',
            color,
            obj.quality_score
        )
    quality_score_display.short_description = '质量评分'


@admin.register(ETLTask)
class ETLTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_name', 'source', 'status_display', 'count_info', 'duration', 'started_at']
    list_filter = ['status', 'started_at']
    search_fields = ['task_name', 'source__name']
    readonly_fields = ['started_at', 'finished_at', 'error_message']
    list_per_page = 30
    date_hierarchy = 'started_at'
    
    fieldsets = (
        ('任务信息', {
            'fields': ('task_name', 'source', 'status')
        }),
        ('执行结果', {
            'fields': ('total_count', 'success_count', 'failed_count')
        }),
        ('时间信息', {
            'fields': ('started_at', 'finished_at')
        }),
        ('错误信息', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )
    
    def status_display(self, obj):
        colors = {
            'running': 'blue',
            'success': 'green',
            'failed': 'red'
        }
        color = colors.get(obj.status, 'black')
        status_text = {
            'running': '运行中',
            'success': '成功',
            'failed': '失败'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status_text.get(obj.status, obj.status)
        )
    status_display.short_description = '状态'
    
    def count_info(self, obj):
        return format_html(
            '总计: <strong>{}</strong><br/>'
            '成功: <span style="color: green;">{}</span><br/>'
            '失败: <span style="color: red;">{}</span>',
            obj.total_count or 0,
            obj.success_count or 0,
            obj.failed_count or 0
        )
    count_info.short_description = '数据统计'
    
    def duration(self, obj):
        if obj.started_at and obj.finished_at:
            delta = obj.finished_at - obj.started_at
            seconds = delta.total_seconds()
            if seconds < 60:
                return f'{int(seconds)}秒'
            elif seconds < 3600:
                return f'{int(seconds/60)}分钟'
            else:
                return f'{int(seconds/3600)}小时{int((seconds%3600)/60)}分钟'
        return '-'
    duration.short_description = '执行时长'

