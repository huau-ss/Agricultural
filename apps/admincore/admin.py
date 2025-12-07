"""
系统管理模块 - Django Admin配置
"""
from django.contrib import admin
from .models import (
    SystemLog, PriceAlert, AlertRule, UserPermission,
    SystemAnnouncement, UserMessage, UserAlertSubscription
)


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['log_type', 'module', 'action', 'user', 'created_at']
    list_filter = ['log_type', 'module', 'created_at']
    search_fields = ['module', 'action', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'region', 'alert_type', 'current_price', 'change_rate', 'status', 'created_at']
    list_filter = ['alert_type', 'status', 'created_at']
    search_fields = ['product_name', 'region', 'message']
    readonly_fields = ['created_at', 'processed_at']


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ['rule_name', 'product_name', 'region', 'alert_type', 'threshold_value', 'is_active', 'created_at']
    list_filter = ['alert_type', 'threshold_type', 'is_active']
    search_fields = ['rule_name', 'product_name', 'region']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SystemAnnouncement)
class SystemAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'announcement_type', 'priority', 'is_published', 'publish_at', 'created_at']
    list_filter = ['announcement_type', 'priority', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'message_type', 'is_read', 'created_at', 'read_at']
    list_filter = ['message_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'content']
    readonly_fields = ['created_at', 'read_at']


@admin.register(UserAlertSubscription)
class UserAlertSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_name', 'region', 'alert_type', 'threshold_value', 'is_active', 'created_at']
    list_filter = ['alert_type', 'threshold_type', 'is_active']
    search_fields = ['user__username', 'product_name', 'region']
    readonly_fields = ['created_at', 'updated_at']

