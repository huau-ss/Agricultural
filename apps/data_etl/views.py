"""
数据采集与清洗模块 - 视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from utils.response import ResponseUtil
from .models import DataSource, RawData, CleanedData, ETLTask
from .serializers import (
    DataSourceSerializer, RawDataSerializer,
    CleanedDataSerializer, ETLTaskSerializer
)


class DataSourceViewSet(viewsets.ModelViewSet):
    """数据源视图集"""
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['source_type', 'status']
    search_fields = ['name', 'url']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def create(self, request, *args, **kwargs):
        """创建数据源"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseUtil.success(data=serializer.data, msg='创建成功')
        return ResponseUtil.error(msg='创建失败', data=serializer.errors)
    
    def retrieve(self, request, *args, **kwargs):
        """详情查询"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def update(self, request, *args, **kwargs):
        """更新数据源"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseUtil.success(data=serializer.data, msg='更新成功')
        return ResponseUtil.error(msg='更新失败', data=serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        """删除数据源"""
        instance = self.get_object()
        instance.delete()
        return ResponseUtil.success(msg='删除成功')
    
    @action(detail=True, methods=['post'])
    def trigger_etl(self, request, pk=None):
        """触发ETL任务"""
        from apps.data_etl.services import ETLService
        
        source = self.get_object()
        try:
            etl_service = ETLService()
            task = etl_service.run_etl_task(source_id=source.id)
            return ResponseUtil.success(
                data={
                    'task_id': task.id,
                    'task_name': task.task_name,
                    'status': task.status,
                    'total_count': task.total_count,
                    'success_count': task.success_count,
                    'failed_count': task.failed_count,
                },
                msg='ETL任务执行完成'
            )
        except Exception as e:
            return ResponseUtil.error(msg=f'ETL任务执行失败: {str(e)}', code=500)


class RawDataViewSet(viewsets.ModelViewSet):
    """原始数据视图集"""
    queryset = RawData.objects.all()
    serializer_class = RawDataSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['source', 'product_name', 'product_category', 'region', 'status']
    search_fields = ['product_name', 'market_name', 'region']
    ordering_fields = ['date', 'created_at', 'price']
    ordering = ['-date', '-created_at']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')


class CleanedDataViewSet(viewsets.ModelViewSet):
    """清洗数据视图集"""
    queryset = CleanedData.objects.all()
    serializer_class = CleanedDataSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_name', 'product_category', 'region']
    search_fields = ['product_name', 'market_name', 'region']
    ordering_fields = ['date', 'price', 'cleaned_at']
    ordering = ['-date']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')


class ETLTaskViewSet(viewsets.ReadOnlyModelViewSet):
    """ETL任务视图集"""
    queryset = ETLTask.objects.all()
    serializer_class = ETLTaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['source', 'status']
    ordering_fields = ['started_at', 'finished_at']
    ordering = ['-started_at']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')

