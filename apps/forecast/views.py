"""
价格预测模块 - 视图
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from utils.response import ResponseUtil
from .models import ForecastModel, ForecastResult, TrainingHistory
from .serializers import (
    ForecastModelSerializer, ForecastResultSerializer,
    TrainingHistorySerializer
)


class ForecastModelViewSet(viewsets.ModelViewSet):
    """预测模型视图集"""
    queryset = ForecastModel.objects.all()
    serializer_class = ForecastModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['model_type', 'product_name', 'region', 'status']
    search_fields = ['model_name', 'product_name', 'region']
    ordering_fields = ['created_at', 'updated_at', 'trained_at']
    ordering = ['-created_at']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseUtil.success(data=serializer.data, msg='创建成功')
        return ResponseUtil.error(msg='创建失败', data=serializer.errors)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseUtil.success(data=serializer.data, msg='更新成功')
        return ResponseUtil.error(msg='更新失败', data=serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return ResponseUtil.success(msg='删除成功')
    
    @action(detail=True, methods=['post'])
    def train(self, request, pk=None):
        """训练模型"""
        model = self.get_object()
        # TODO: 调用训练脚本
        return ResponseUtil.success(msg='模型训练已启动')
    
    @action(detail=True, methods=['post'])
    def predict(self, request, pk=None):
        """执行预测"""
        model = self.get_object()
        days = request.data.get('days', 7)  # 默认预测7天
        # TODO: 调用预测算法
        return ResponseUtil.success(msg='预测任务已启动', data={'days': days})


class ForecastResultViewSet(viewsets.ReadOnlyModelViewSet):
    """预测结果视图集"""
    queryset = ForecastResult.objects.all()
    serializer_class = ForecastResultSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['model', 'product_name', 'region']
    search_fields = ['product_name', 'region']
    ordering_fields = ['forecast_date', 'created_at']
    ordering = ['-forecast_date']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # 时间范围过滤
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(forecast_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(forecast_date__lte=end_date)
        
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    @action(detail=False, methods=['get'])
    def accuracy_analysis(self, request):
        """预测准确度分析"""
        product_name = request.query_params.get('product_name')
        region = request.query_params.get('region')
        
        queryset = ForecastResult.objects.filter(actual_price__isnull=False)
        if product_name:
            queryset = queryset.filter(product_name=product_name)
        if region:
            queryset = queryset.filter(region=region)
        
        # 计算准确度指标
        results = []
        for result in queryset:
            if result.actual_price and result.forecast_price:
                error = abs(float(result.forecast_price) - float(result.actual_price))
                error_rate = (error / float(result.actual_price)) * 100
                results.append({
                    'forecast_date': result.forecast_date,
                    'forecast_price': float(result.forecast_price),
                    'actual_price': float(result.actual_price),
                    'error': float(error),
                    'error_rate': error_rate,
                })
        
        return ResponseUtil.success(data=results, msg='查询成功')


class TrainingHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """训练历史视图集"""
    queryset = TrainingHistory.objects.all()
    serializer_class = TrainingHistorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['model', 'status']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')

