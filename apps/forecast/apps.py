from django.apps import AppConfig


class ForecastConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.forecast'
    verbose_name = '价格预测'
    
    def ready(self):
        import apps.forecast.signals  # 注册信号

