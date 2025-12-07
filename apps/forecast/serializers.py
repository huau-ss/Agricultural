"""
价格预测模块 - 序列化器
"""
from rest_framework import serializers
from .models import ForecastModel, ForecastResult, TrainingHistory


class ForecastModelSerializer(serializers.ModelSerializer):
    """预测模型序列化器"""
    
    class Meta:
        model = ForecastModel
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'trained_at']


class ForecastResultSerializer(serializers.ModelSerializer):
    """预测结果序列化器"""
    model_name = serializers.CharField(source='model.model_name', read_only=True)
    model_type = serializers.CharField(source='model.model_type', read_only=True)
    
    class Meta:
        model = ForecastResult
        fields = '__all__'
        read_only_fields = ['created_at']


class TrainingHistorySerializer(serializers.ModelSerializer):
    """训练历史序列化器"""
    model_name = serializers.CharField(source='model.model_name', read_only=True)
    
    class Meta:
        model = TrainingHistory
        fields = '__all__'
        read_only_fields = ['created_at']

