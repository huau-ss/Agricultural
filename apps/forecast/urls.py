"""
价格预测模块 - URL路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ForecastModelViewSet, ForecastResultViewSet, TrainingHistoryViewSet

router = DefaultRouter()
router.register(r'models', ForecastModelViewSet, basename='forecastmodel')
router.register(r'results', ForecastResultViewSet, basename='forecastresult')
router.register(r'training-history', TrainingHistoryViewSet, basename='traininghistory')

urlpatterns = [
    path('', include(router.urls)),
]

