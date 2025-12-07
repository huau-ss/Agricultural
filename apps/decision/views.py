"""
决策辅助模块 - 视图
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from decimal import Decimal
from utils.response import ResponseUtil
from .models import ProfitSimulation, DecisionAdvice
from .serializers import ProfitSimulationSerializer, DecisionAdviceSerializer


class ProfitSimulationViewSet(viewsets.ModelViewSet):
    """利润模拟视图集"""
    queryset = ProfitSimulation.objects.all()
    serializer_class = ProfitSimulationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_name', 'region']
    search_fields = ['product_name', 'region']
    ordering_fields = ['simulation_date', 'profit', 'profit_rate']
    ordering = ['-simulation_date', '-created_at']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def create(self, request, *args, **kwargs):
        """创建利润模拟（自动计算）"""
        data = request.data.copy()
        
        # 计算总成本和总收入
        purchase_price = Decimal(str(data.get('purchase_price', 0)))
        sale_price = Decimal(str(data.get('sale_price', 0)))
        quantity = Decimal(str(data.get('quantity', 0)))
        transport_cost = Decimal(str(data.get('transport_cost', 0)))
        storage_cost = Decimal(str(data.get('storage_cost', 0)))
        other_cost = Decimal(str(data.get('other_cost', 0)))
        
        total_cost = purchase_price * quantity + transport_cost + storage_cost + other_cost
        total_revenue = sale_price * quantity
        profit = total_revenue - total_cost
        profit_rate = (profit / total_cost * 100) if total_cost > 0 else 0
        
        data['total_cost'] = str(total_cost)
        data['total_revenue'] = str(total_revenue)
        data['profit'] = str(profit)
        data['profit_rate'] = float(profit_rate)
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return ResponseUtil.success(data=serializer.data, msg='模拟成功')
        return ResponseUtil.error(msg='模拟失败', data=serializer.errors)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    @action(detail=False, methods=['post'])
    def batch_simulate(self, request):
        """批量利润模拟"""
        scenarios = request.data.get('scenarios', [])
        results = []
        
        for scenario in scenarios:
            purchase_price = Decimal(str(scenario.get('purchase_price', 0)))
            sale_price = Decimal(str(scenario.get('sale_price', 0)))
            quantity = Decimal(str(scenario.get('quantity', 0)))
            transport_cost = Decimal(str(scenario.get('transport_cost', 0)))
            storage_cost = Decimal(str(scenario.get('storage_cost', 0)))
            other_cost = Decimal(str(scenario.get('other_cost', 0)))
            
            total_cost = purchase_price * quantity + transport_cost + storage_cost + other_cost
            total_revenue = sale_price * quantity
            profit = total_revenue - total_cost
            profit_rate = (profit / total_cost * 100) if total_cost > 0 else 0
            
            results.append({
                **scenario,
                'total_cost': float(total_cost),
                'total_revenue': float(total_revenue),
                'profit': float(profit),
                'profit_rate': float(profit_rate),
            })
        
        return ResponseUtil.success(data=results, msg='批量模拟成功')


class DecisionAdviceViewSet(viewsets.ModelViewSet):
    """决策建议视图集"""
    queryset = DecisionAdvice.objects.all()
    serializer_class = DecisionAdviceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_name', 'region', 'advice_type']
    search_fields = ['product_name', 'region', 'advice_content']
    ordering_fields = ['created_at', 'confidence']
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
    
    @action(detail=False, methods=['post'])
    def generate_advice(self, request):
        """生成决策建议"""
        product_name = request.data.get('product_name')
        region = request.data.get('region')
        advice_type = request.data.get('advice_type', 'purchase')
        
        # TODO: 调用决策算法生成建议
        # 这里先返回示例数据
        advice_content = f"基于当前市场数据，建议对{product_name}采取{advice_type}策略。"
        
        advice = DecisionAdvice.objects.create(
            product_name=product_name,
            region=region,
            advice_type=advice_type,
            advice_content=advice_content,
            confidence=0.75,
            factors=['价格趋势', '供需关系', '季节性因素']
        )
        
        serializer = self.get_serializer(advice)
        return ResponseUtil.success(data=serializer.data, msg='建议生成成功')

