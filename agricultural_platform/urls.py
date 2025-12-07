"""
URL configuration for agricultural_platform project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def index(request):
    """首页"""
    return HttpResponse("""
    <h1>农产品产销分析与辅助决策平台</h1>
    <ul>
        <li><a href="/admin/">管理后台</a></li>
        <li><a href="/api/data-etl/sources/">数据源API</a></li>
        <li><a href="/api/market/prices/">市场价格API</a></li>
    </ul>
    """)

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/data-etl/', include('apps.data_etl.urls')),
    path('api/market/', include('apps.market.urls')),
    path('api/forecast/', include('apps.forecast.urls')),
    path('api/decision/', include('apps.decision.urls')),
    path('api/trade/', include('apps.trade.urls')),
    path('api/admincore/', include('apps.admincore.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

