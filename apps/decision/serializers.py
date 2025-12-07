"""
决策辅助模块 - 序列化器
"""
from rest_framework import serializers
from .models import ProfitSimulation, DecisionAdvice


class ProfitSimulationSerializer(serializers.ModelSerializer):
    """利润模拟序列化器"""
    
    class Meta:
        model = ProfitSimulation
        fields = '__all__'
        read_only_fields = ['created_at']


class DecisionAdviceSerializer(serializers.ModelSerializer):
    """决策建议序列化器"""
    
    class Meta:
        model = DecisionAdvice
        fields = '__all__'
        read_only_fields = ['created_at']

