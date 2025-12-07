"""
供需对接模块 - URL路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplyInfoViewSet, DemandInfoViewSet, TradeMatchViewSet

router = DefaultRouter()
router.register(r'supplies', SupplyInfoViewSet, basename='supplyinfo')
router.register(r'demands', DemandInfoViewSet, basename='demandinfo')
router.register(r'matches', TradeMatchViewSet, basename='tradematch')

urlpatterns = [
    path('', include(router.urls)),
]

