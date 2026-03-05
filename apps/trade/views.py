"""
供需对接模块 - 视图
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from utils.response import ResponseUtil
from .models import SupplyInfo, DemandInfo, TradeMatch
from .serializers import SupplyInfoSerializer, DemandInfoSerializer, TradeMatchSerializer


class SupplyInfoViewSet(viewsets.ModelViewSet):
    """供应信息视图集"""
    queryset = SupplyInfo.objects.filter(status='active')
    serializer_class = SupplyInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_name', 'product_category', 'region', 'status']
    search_fields = ['product_name', 'region', 'contact_name']
    ordering_fields = ['created_at', 'price', 'quantity']
    ordering = ['-created_at']
    
    def list(self, request, *args, **kwargs):
        """列表查询（支持分页）"""
        from utils.pagination import StandardResultsSetPagination
        
        queryset = self.filter_queryset(self.get_queryset())
        
        # 分页
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # 无分页
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseUtil.success(data=serializer.data, msg='发布成功')
        return ResponseUtil.error(msg='发布失败', data=serializer.errors)
    
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
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """标记为已完成"""
        instance = self.get_object()
        instance.status = 'completed'
        instance.save()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='操作成功')


class DemandInfoViewSet(viewsets.ModelViewSet):
    """需求信息视图集"""
    queryset = DemandInfo.objects.filter(status='active')
    serializer_class = DemandInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_name', 'product_category', 'region', 'status']
    search_fields = ['product_name', 'region', 'contact_name']
    ordering_fields = ['created_at', 'max_price', 'quantity']
    ordering = ['-created_at']
    
    def list(self, request, *args, **kwargs):
        """列表查询（支持分页）"""
        from utils.pagination import StandardResultsSetPagination
        
        queryset = self.filter_queryset(self.get_queryset())
        
        # 分页
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # 无分页
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ResponseUtil.success(data=serializer.data, msg='发布成功')
        return ResponseUtil.error(msg='发布失败', data=serializer.errors)
    
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
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """标记为已完成"""
        instance = self.get_object()
        instance.status = 'completed'
        instance.save()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='操作成功')


class TradeMatchViewSet(viewsets.ModelViewSet):
    """交易匹配视图集"""
    queryset = TradeMatch.objects.all()
    serializer_class = TradeMatchSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['supply', 'demand', 'status']
    ordering_fields = ['match_score', 'created_at']
    ordering = ['-match_score', '-created_at']
    
    def list(self, request, *args, **kwargs):
        """列表查询（支持分页和自动匹配）"""
        from utils.pagination import StandardResultsSetPagination
        
        queryset = self.filter_queryset(self.get_queryset())
        
        # 自动匹配：如果没有匹配记录，尝试创建新的匹配
        if queryset.count() == 0:
            self._auto_match()
            queryset = self.filter_queryset(self.get_queryset())
        
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
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    @action(detail=False, methods=['post'])
    def match(self, request):
        """执行匹配"""
        supply_id = request.data.get('supply_id')
        demand_id = request.data.get('demand_id')
        
        if not supply_id or not demand_id:
            return ResponseUtil.error(msg='请提供供应和需求ID')
        
        try:
            supply = SupplyInfo.objects.get(id=supply_id, status='active')
            demand = DemandInfo.objects.get(id=demand_id, status='active')
        except (SupplyInfo.DoesNotExist, DemandInfo.DoesNotExist):
            return ResponseUtil.error(msg='供应或需求信息不存在或已失效')
        
        # 计算匹配度
        match_score = self._calculate_match_score(supply, demand)
        
        match, created = TradeMatch.objects.get_or_create(
            supply=supply,
            demand=demand,
            defaults={
                'match_score': match_score,
                'status': 'pending'
            }
        )
        
        if not created:
            match.match_score = match_score
            match.save()
        
        serializer = self.get_serializer(match)
        return ResponseUtil.success(data=serializer.data, msg='匹配成功')
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """确认匹配"""
        match = self.get_object()
        match.status = 'confirmed'
        match.confirmed_at = timezone.now()
        match.save()
        
        # 更新供应和需求状态
        match.supply.status = 'completed'
        match.supply.save()
        match.demand.status = 'completed'
        match.demand.save()
        
        serializer = self.get_serializer(match)
        return ResponseUtil.success(data=serializer.data, msg='确认成功')
    
    def _auto_match(self):
        """自动匹配供应和需求"""
        supplies = SupplyInfo.objects.filter(status='active')[:10]
        demands = DemandInfo.objects.filter(status='active')[:10]
        
        for supply in supplies:
            for demand in demands:
                # 检查是否已匹配
                if TradeMatch.objects.filter(supply=supply, demand=demand).exists():
                    continue
                
                # 计算匹配度
                match_score = self._calculate_match_score(supply, demand)
                
                # 如果匹配度大于60，创建匹配记录
                if match_score >= 60:
                    TradeMatch.objects.create(
                        supply=supply,
                        demand=demand,
                        match_score=match_score,
                        status='pending'
                    )
    
    def _calculate_match_score(self, supply, demand):
        """计算匹配度"""
        score = 0.0
        
        # 产品名称匹配
        if supply.product_name == demand.product_name:
            score += 40
        elif supply.product_category == demand.product_category:
            score += 20
        
        # 地区匹配
        if supply.region == demand.region:
            score += 30
        else:
            score += 10
        
        # 价格匹配
        if demand.max_price:
            if supply.price <= demand.max_price:
                price_ratio = float(supply.price) / float(demand.max_price)
                score += 30 * (1 - price_ratio)
        else:
            score += 15
        
        # 数量匹配
        if supply.quantity >= demand.quantity:
            score += 20
        else:
            quantity_ratio = float(supply.quantity) / float(demand.quantity)
            score += 20 * quantity_ratio
        
        return min(score, 100.0)
