"""
市场行情模块 - 序列化器
"""
from rest_framework import serializers
from .models import MarketPrice, MarketStatistics


class MarketPriceSerializer(serializers.ModelSerializer):
    """市场价格序列化器"""
    
    class Meta:
        model = MarketPrice
        fields = '__all__'
        read_only_fields = ['created_at']


class MarketStatisticsSerializer(serializers.ModelSerializer):
    """市场统计序列化器"""
    
    class Meta:
        model = MarketStatistics
        fields = '__all__'
        read_only_fields = ['created_at']

