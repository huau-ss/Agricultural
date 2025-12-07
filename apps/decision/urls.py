"""
决策辅助模块 - URL路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfitSimulationViewSet, DecisionAdviceViewSet

router = DefaultRouter()
router.register(r'profit-simulations', ProfitSimulationViewSet, basename='profitsimulation')
router.register(r'advices', DecisionAdviceViewSet, basename='decisionadvice')

urlpatterns = [
    path('', include(router.urls)),
]

