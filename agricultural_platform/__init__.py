"""
Django项目初始化
"""
# 在Django启动时自动启动定时任务调度器
import os
import logging

logger = logging.getLogger(__name__)

# 只在主进程中启动调度器（避免在开发模式下启动两次）
if os.environ.get('RUN_MAIN') == 'true':
    from django.conf import settings
    
    # 检查是否启用定时任务
    if getattr(settings, 'ENABLE_SCHEDULER', True):
        try:
            from apps.data_etl.scheduler import start_scheduler
            logger.info("正在启动定时任务调度器...")
            start_scheduler()
        except Exception as e:
            logger.error(f"定时任务调度器启动失败: {str(e)}")
