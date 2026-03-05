"""
市场行情模块 - 视图
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Max, Min, StdDev, Count
from django.utils import timezone
from datetime import timedelta
from utils.response import ResponseUtil
from .models import MarketPrice, MarketStatistics
from .serializers import MarketPriceSerializer, MarketStatisticsSerializer


class MarketPriceViewSet(viewsets.ModelViewSet):
    """市场价格视图集"""
    queryset = MarketPrice.objects.all()
    serializer_class = MarketPriceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_name', 'product_category', 'region', 'market_name']
    search_fields = ['product_name', 'market_name', 'region']
    ordering_fields = ['date', 'price', 'created_at']
    ordering = ['-date', 'product_name']
    
    def list(self, request, *args, **kwargs):
        """列表查询"""
        from utils.pagination import StandardResultsSetPagination
        
        queryset = self.filter_queryset(self.get_queryset())
        
        # 时间范围过滤
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # 分页
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # 无分页
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def retrieve(self, request, *args, **kwargs):
        """详情查询"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """市场行情驾驶舱数据"""
        # 获取最近30天的数据
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        # 统计信息
        total_count = MarketPrice.objects.count()
        product_count = MarketPrice.objects.values('product_name').distinct().count()
        market_count = MarketPrice.objects.values('market_name').distinct().count()
        
        # 预警数量（从admincore获取）
        try:
            from apps.admincore.models import PriceAlert
            alert_count = PriceAlert.objects.filter(status='pending').count()
        except:
            alert_count = 0
        
        # 按产品统计
        product_stats = MarketPrice.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).values('product_name').annotate(
            avg_price=Avg('price'),
            max_price=Max('price'),
            min_price=Min('price'),
            count=Count('id')
        ).order_by('-count')[:10]  # 取前10个
        
        # 按地区统计
        region_stats = MarketPrice.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).values('region').annotate(
            avg_price=Avg('price'),
            count=Count('id')
        ).order_by('-count')[:10]  # 取前10个
        
        # 价格趋势（按日期，取最近30天）
        price_trend = MarketPrice.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).values('date').annotate(
            avg_price=Avg('price')
        ).order_by('date')
        
        # 转换价格趋势格式
        price_trend_list = []
        for item in price_trend:
            price_trend_list.append({
                'date': item['date'].strftime('%Y-%m-%d') if hasattr(item['date'], 'strftime') else str(item['date']),
                'price': float(item['avg_price'])
            })
        
        return ResponseUtil.success(data={
            'total_count': total_count,
            'product_count': product_count,
            'market_count': market_count,
            'alert_count': alert_count,
            'product_stats': [
                {
                    'product_name': item['product_name'],
                    'avg_price': float(item['avg_price']),
                    'max_price': float(item['max_price']),
                    'min_price': float(item['min_price']),
                    'count': item['count']
                }
                for item in product_stats
            ],
            'region_stats': [
                {
                    'region': item['region'],
                    'avg_price': float(item['avg_price']),
                    'count': item['count']
                }
                for item in region_stats
            ],
            'price_trend': price_trend_list,
        }, msg='查询成功')
    
    @action(detail=False, methods=['get'])
    def price_comparison(self, request):
        """价格对比数据"""
        product_name = request.query_params.get('product_name')
        regions = request.query_params.getlist('regions')
        
        if not product_name:
            return ResponseUtil.error(msg='请指定农产品名称')
        
        queryset = MarketPrice.objects.filter(product_name=product_name)
        if regions:
            queryset = queryset.filter(region__in=regions)
        
        # 按地区和日期分组
        comparison_data = queryset.values('region', 'date').annotate(
            avg_price=Avg('price')
        ).order_by('date', 'region')
        
        return ResponseUtil.success(data=list(comparison_data), msg='查询成功')


class MarketStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """市场统计视图集"""
    queryset = MarketStatistics.objects.all()
    serializer_class = MarketStatisticsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_name', 'product_category', 'region', 'stat_type']
    search_fields = ['product_name', 'region']
    ordering_fields = ['stat_date']
    ordering = ['-stat_date']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')

