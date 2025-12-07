"""
Django Admin 自定义配置
"""
from django.contrib import admin
from django.contrib.admin import AdminSite

admin.site.site_header = '农产品产销分析与辅助决策平台'
admin.site.site_title = '管理后台'
admin.site.index_title = '欢迎使用管理后台'

