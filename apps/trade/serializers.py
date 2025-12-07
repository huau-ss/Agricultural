"""
供需对接模块 - 序列化器
"""
from rest_framework import serializers
from .models import SupplyInfo, DemandInfo, TradeMatch


class SupplyInfoSerializer(serializers.ModelSerializer):
    """供应信息序列化器"""
    
    class Meta:
        model = SupplyInfo
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class DemandInfoSerializer(serializers.ModelSerializer):
    """需求信息序列化器"""
    
    class Meta:
        model = DemandInfo
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TradeMatchSerializer(serializers.ModelSerializer):
    """交易匹配序列化器"""
    supply_product = serializers.CharField(source='supply.product_name', read_only=True)
    demand_product = serializers.CharField(source='demand.product_name', read_only=True)
    
    class Meta:
        model = TradeMatch
        fields = '__all__'
        read_only_fields = ['created_at', 'confirmed_at']

