"""
市场行情模块 - URL路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarketPriceViewSet, MarketStatisticsViewSet

router = DefaultRouter()
router.register(r'prices', MarketPriceViewSet, basename='marketprice')
router.register(r'statistics', MarketStatisticsViewSet, basename='marketstatistics')

urlpatterns = [
    path('', include(router.urls)),
]

