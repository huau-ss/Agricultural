"""
系统管理模块 - Django Admin配置
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SystemLog, PriceAlert, AlertRule, UserPermission,
    SystemAnnouncement, UserMessage, UserAlertSubscription
)


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'log_type_display', 'module', 'action', 'user', 'ip_address', 'created_at']
    list_filter = ['log_type', 'module', 'created_at']
    search_fields = ['module', 'action', 'message', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    def log_type_display(self, obj):
        colors = {
            'info': 'blue',
            'warning': 'orange',
            'error': 'red',
            'debug': 'gray'
        }
        color = colors.get(obj.log_type, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_log_type_display()
        )
    log_type_display.short_description = '日志类型'


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'region', 'alert_type_display', 'price_info', 'change_rate_display', 'status_display', 'created_at']
    list_filter = ['alert_type', 'status', 'created_at']
    search_fields = ['product_name', 'region', 'message']
    readonly_fields = ['created_at', 'processed_at']
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    def alert_type_display(self, obj):
        color = 'red' if obj.alert_type == 'price_rise' else 'green'
        text = '价格上涨' if obj.alert_type == 'price_rise' else '价格下跌'
        return format_html('<span style="color: {};">{}</span>', color, text)
    alert_type_display.short_description = '预警类型'
    
    def price_info(self, obj):
        return format_html('当前: ¥{}<br/>阈值: ¥{}', obj.current_price, obj.threshold_price)
    price_info.short_description = '价格信息'
    
    def change_rate_display(self, obj):
        color = 'red' if obj.change_rate >= 0 else 'green'
        symbol = '+' if obj.change_rate >= 0 else ''
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}{:.2f}%</span>',
            color,
            symbol,
            obj.change_rate
        )
    change_rate_display.short_description = '变化率'
    
    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'processed': 'green',
            'ignored': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = '状态'


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'rule_name', 'product_name', 'region', 'alert_type', 'threshold_display', 'is_active_display', 'created_at']
    list_filter = ['alert_type', 'threshold_type', 'is_active', 'created_at']
    search_fields = ['rule_name', 'product_name', 'region']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 30
    
    def threshold_display(self, obj):
        return format_html('{} {}', obj.threshold_value, obj.get_threshold_type_display())
    threshold_display.short_description = '阈值'
    
    def is_active_display(self, obj):
        color = 'green' if obj.is_active else 'gray'
        text = '启用' if obj.is_active else '禁用'
        return format_html('<span style="color: {};">{}</span>', color, text)
    is_active_display.short_description = '状态'


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role', 'permissions_list', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 30
    
    def permissions_list(self, obj):
        if obj.permissions:
            perms = obj.permissions if isinstance(obj.permissions, list) else []
            return ', '.join(perms[:3]) + ('...' if len(perms) > 3 else '')
        return '-'
    permissions_list.short_description = '权限列表'


@admin.register(SystemAnnouncement)
class SystemAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'announcement_type', 'priority_display', 'is_published_display', 'publish_at', 'created_at']
    list_filter = ['announcement_type', 'priority', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'content', 'announcement_type', 'priority')
        }),
        ('发布设置', {
            'fields': ('is_published', 'publish_at', 'expire_at')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def priority_display(self, obj):
        colors = {
            'high': 'red',
            'medium': 'orange',
            'low': 'blue'
        }
        color = colors.get(obj.priority, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_display.short_description = '优先级'
    
    def is_published_display(self, obj):
        if obj.is_published:
            return format_html('<span style="color: green;">✓ 已发布</span>')
        return format_html('<span style="color: gray;">未发布</span>')
    is_published_display.short_description = '发布状态'


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'message_type', 'is_read_display', 'created_at', 'read_at']
    list_filter = ['message_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'content']
    readonly_fields = ['created_at', 'read_at']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    def is_read_display(self, obj):
        if obj.is_read:
            return format_html('<span style="color: green;">✓ 已读</span>')
        return format_html('<span style="color: red;">未读</span>')
    is_read_display.short_description = '阅读状态'


@admin.register(UserAlertSubscription)
class UserAlertSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_name', 'region', 'alert_type', 'threshold_display', 'is_active_display', 'created_at']
    list_filter = ['alert_type', 'threshold_type', 'is_active', 'created_at']
    search_fields = ['user__username', 'product_name', 'region']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 30
    
    def threshold_display(self, obj):
        return format_html('{} {}', obj.threshold_value, obj.get_threshold_type_display())
    threshold_display.short_description = '阈值'
    
    def is_active_display(self, obj):
        color = 'green' if obj.is_active else 'gray'
        text = '启用' if obj.is_active else '禁用'
        return format_html('<span style="color: {};">{}</span>', color, text)
    is_active_display.short_description = '状态'

