"""
预测模块信号
当预测结果创建时，自动触发预警检查
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ForecastResult
from apps.admincore.services import AlertService
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ForecastResult)
def check_forecast_alert(sender, instance, created, **kwargs):
    """
    当创建新的预测结果时，检查是否需要生成预警
    """
    if created:
        try:
            # 异步检查预警（避免阻塞）
            # 实际生产环境可以使用Celery异步任务
            AlertService.check_forecast_alerts()
            logger.info(f"预测结果创建后触发预警检查: {instance.product_name}")
        except Exception as e:
            logger.error(f"预警检查失败: {str(e)}")

