"""
系统管理模块 - 视图
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from django.utils import timezone
from utils.response import ResponseUtil
from .models import (
    SystemLog, PriceAlert, AlertRule, UserPermission,
    SystemAnnouncement, UserMessage, UserAlertSubscription
)
from .serializers import (
    SystemLogSerializer, PriceAlertSerializer,
    AlertRuleSerializer, UserPermissionSerializer, UserSerializer,
    SystemAnnouncementSerializer, UserMessageSerializer, UserAlertSubscriptionSerializer
)
from .services import AlertService, MessageService


class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    """系统日志视图集"""
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['log_type', 'module']
    search_fields = ['module', 'action', 'message']
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


class PriceAlertViewSet(viewsets.ModelViewSet):
    """价格预警视图集"""
    queryset = PriceAlert.objects.all()
    serializer_class = PriceAlertSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_name', 'region', 'alert_type', 'status']
    search_fields = ['product_name', 'region', 'message']
    ordering_fields = ['created_at', 'change_rate']
    ordering = ['-created_at']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """处理预警"""
        instance = self.get_object()
        instance.status = 'processed'
        instance.processed_at = timezone.now()
        instance.save()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='处理成功')
    
    @action(detail=True, methods=['post'])
    def ignore(self, request, pk=None):
        """忽略预警"""
        instance = self.get_object()
        instance.status = 'ignored'
        instance.processed_at = timezone.now()
        instance.save()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='已忽略')


class AlertRuleViewSet(viewsets.ModelViewSet):
    """预警规则视图集"""
    queryset = AlertRule.objects.all()
    serializer_class = AlertRuleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_name', 'region', 'alert_type', 'is_active']
    search_fields = ['rule_name', 'product_name', 'region']
    ordering_fields = ['created_at', 'updated_at']
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


class UserPermissionViewSet(viewsets.ModelViewSet):
    """用户权限视图集"""
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role']
    search_fields = ['user__username']
    ordering_fields = ['created_at']
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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """用户视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering_fields = ['date_joined']
    ordering = ['-date_joined']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')


class SystemAnnouncementViewSet(viewsets.ModelViewSet):
    """系统公告视图集"""
    queryset = SystemAnnouncement.objects.all()
    serializer_class = SystemAnnouncementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['announcement_type', 'priority', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'publish_at', 'priority']
    ordering = ['-priority', '-created_at']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 默认只显示已发布的公告
        if not request.query_params.get('all'):
            queryset = queryset.filter(is_published=True)
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user if request.user.is_authenticated else None)
            return ResponseUtil.success(data=serializer.data, msg='创建成功')
        return ResponseUtil.error(msg='创建失败', data=serializer.errors)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布公告"""
        instance = self.get_object()
        instance.is_published = True
        instance.publish_at = timezone.now()
        instance.save()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='发布成功')
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """取消发布"""
        instance = self.get_object()
        instance.is_published = False
        instance.save()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='取消发布成功')


class UserMessageViewSet(viewsets.ModelViewSet):
    """站内信视图集"""
    serializer_class = UserMessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['message_type', 'is_read']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'read_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """只返回当前用户的消息"""
        if self.request.user.is_authenticated:
            return UserMessage.objects.filter(user=self.request.user)
        return UserMessage.objects.none()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        # 获取未读数量
        unread_count = MessageService.get_unread_count(request.user) if request.user.is_authenticated else 0
        
        return ResponseUtil.success(data={
            'results': serializer.data,
            'unread_count': unread_count
        }, msg='查询成功')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 标记为已读
        if not instance.is_read:
            MessageService.mark_as_read(instance.id, request.user)
            instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """获取未读消息数量"""
        if not request.user.is_authenticated:
            return ResponseUtil.error(msg='未登录', code=401)
        count = MessageService.get_unread_count(request.user)
        return ResponseUtil.success(data={'count': count}, msg='查询成功')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """标记为已读"""
        instance = self.get_object()
        if MessageService.mark_as_read(instance.id, request.user):
            serializer = self.get_serializer(instance)
            return ResponseUtil.success(data=serializer.data, msg='标记成功')
        return ResponseUtil.error(msg='标记失败')
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """标记所有为已读"""
        if not request.user.is_authenticated:
            return ResponseUtil.error(msg='未登录', code=401)
        count = MessageService.mark_all_as_read(request.user)
        return ResponseUtil.success(data={'count': count}, msg='标记成功')


class UserAlertSubscriptionViewSet(viewsets.ModelViewSet):
    """用户预警订阅视图集"""
    serializer_class = UserAlertSubscriptionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_name', 'region', 'alert_type', 'is_active']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """只返回当前用户的订阅"""
        if self.request.user.is_authenticated:
            return UserAlertSubscription.objects.filter(user=self.request.user)
        return UserAlertSubscription.objects.none()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ResponseUtil.success(data=serializer.data, msg='查询成功')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user if request.user.is_authenticated else None)
            return ResponseUtil.success(data=serializer.data, msg='订阅成功')
        return ResponseUtil.error(msg='订阅失败', data=serializer.errors)
    
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
        return ResponseUtil.success(msg='取消订阅成功')


class AlertCheckViewSet(viewsets.ViewSet):
    """预警检查视图集"""
    
    @action(detail=False, methods=['post'])
    def check_forecast(self, request):
        """检查预测预警"""
        count = AlertService.check_forecast_alerts()
        return ResponseUtil.success(data={'alerts_created': count}, msg='预警检查完成')
    
    @action(detail=False, methods=['post'])
    def check_price_change(self, request):
        """检查价格变化预警"""
        count = AlertService.check_price_change_alerts()
        return ResponseUtil.success(data={'alerts_created': count}, msg='预警检查完成')

