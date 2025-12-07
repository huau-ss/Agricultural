"""
系统管理模块 - 序列化器
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    SystemLog, PriceAlert, AlertRule, UserPermission,
    SystemAnnouncement, UserMessage, UserAlertSubscription
)


class SystemLogSerializer(serializers.ModelSerializer):
    """系统日志序列化器"""
    username = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    
    class Meta:
        model = SystemLog
        fields = '__all__'
        read_only_fields = ['created_at']


class PriceAlertSerializer(serializers.ModelSerializer):
    """价格预警序列化器"""
    
    class Meta:
        model = PriceAlert
        fields = '__all__'
        read_only_fields = ['created_at', 'processed_at']


class AlertRuleSerializer(serializers.ModelSerializer):
    """预警规则序列化器"""
    
    class Meta:
        model = AlertRule
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class UserPermissionSerializer(serializers.ModelSerializer):
    """用户权限序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserPermission
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
        read_only_fields = ['date_joined']


class SystemAnnouncementSerializer(serializers.ModelSerializer):
    """系统公告序列化器"""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = SystemAnnouncement
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class UserMessageSerializer(serializers.ModelSerializer):
    """站内信序列化器"""
    related_alert_id = serializers.IntegerField(source='related_alert.id', read_only=True, allow_null=True)
    
    class Meta:
        model = UserMessage
        fields = '__all__'
        read_only_fields = ['created_at', 'read_at']


class UserAlertSubscriptionSerializer(serializers.ModelSerializer):
    """用户预警订阅序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserAlertSubscription
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

