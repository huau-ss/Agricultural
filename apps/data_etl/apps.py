from django.apps import AppConfig


class DataEtlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.data_etl'
    verbose_name = '数据采集与清洗'

