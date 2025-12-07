"""
数据采集与清洗模块 - 序列化器
"""
from rest_framework import serializers
from .models import DataSource, RawData, CleanedData, ETLTask


class DataSourceSerializer(serializers.ModelSerializer):
    """数据源序列化器"""
    
    class Meta:
        model = DataSource
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class RawDataSerializer(serializers.ModelSerializer):
    """原始数据序列化器"""
    source_name = serializers.CharField(source='source.name', read_only=True)
    
    class Meta:
        model = RawData
        fields = '__all__'
        read_only_fields = ['created_at']


class CleanedDataSerializer(serializers.ModelSerializer):
    """清洗数据序列化器"""
    
    class Meta:
        model = CleanedData
        fields = '__all__'
        read_only_fields = ['cleaned_at']


class ETLTaskSerializer(serializers.ModelSerializer):
    """ETL任务序列化器"""
    source_name = serializers.CharField(source='source.name', read_only=True, allow_null=True)
    
    class Meta:
        model = ETLTask
        fields = '__all__'
        read_only_fields = ['started_at', 'finished_at']

