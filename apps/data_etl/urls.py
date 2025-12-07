"""
数据采集与清洗模块 - URL路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataSourceViewSet, RawDataViewSet, CleanedDataViewSet, ETLTaskViewSet

router = DefaultRouter()
router.register(r'sources', DataSourceViewSet, basename='datasource')
router.register(r'raw-data', RawDataViewSet, basename='rawdata')
router.register(r'cleaned-data', CleanedDataViewSet, basename='cleaneddata')
router.register(r'tasks', ETLTaskViewSet, basename='etltask')

urlpatterns = [
    path('', include(router.urls)),
]

