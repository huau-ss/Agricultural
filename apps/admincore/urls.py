"""
系统管理模块 - URL路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SystemLogViewSet, PriceAlertViewSet, AlertRuleViewSet,
    UserPermissionViewSet, UserViewSet,
    SystemAnnouncementViewSet, UserMessageViewSet,
    UserAlertSubscriptionViewSet, AlertCheckViewSet
)

router = DefaultRouter()
router.register(r'logs', SystemLogViewSet, basename='systemlog')
router.register(r'alerts', PriceAlertViewSet, basename='pricealert')
router.register(r'alert-rules', AlertRuleViewSet, basename='alertrule')
router.register(r'permissions', UserPermissionViewSet, basename='userpermission')
router.register(r'users', UserViewSet, basename='user')
router.register(r'announcements', SystemAnnouncementViewSet, basename='announcement')
router.register(r'messages', UserMessageViewSet, basename='usermessage')
router.register(r'alert-subscriptions', UserAlertSubscriptionViewSet, basename='alertsubscription')
router.register(r'alert-check', AlertCheckViewSet, basename='alertcheck')

urlpatterns = [
    path('', include(router.urls)),
]

