"""
定时任务调度器 - 使用APScheduler
"""
import logging
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings
from apps.data_etl.tasks import daily_data_collection_task

logger = logging.getLogger(__name__)

# 全局调度器实例
scheduler = None


def start_scheduler():
    """
    启动定时任务调度器
    """
    global scheduler
    
    if scheduler and scheduler.running:
        logger.warning("定时任务调度器已在运行")
        return scheduler
    
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # 注册定时任务
    # 每天凌晨2点执行数据采集
    scheduler.add_job(
        daily_data_collection_task,
        trigger=CronTrigger(hour=2, minute=0),  # 每天凌晨2点
        id='daily_data_collection',
        name='每日数据采集-凌晨',
        replace_existing=True,
        max_instances=1,  # 同一时间只允许一个实例运行
    )
    
    # 每天上午10点执行数据采集
    scheduler.add_job(
        daily_data_collection_task,
        trigger=CronTrigger(hour=10, minute=0),  # 每天上午10点
        id='daily_data_collection_morning',
        name='每日数据采集-上午',
        replace_existing=True,
        max_instances=1,
    )
    
    # 每天下午6点执行数据采集
    scheduler.add_job(
        daily_data_collection_task,
        trigger=CronTrigger(hour=18, minute=0),  # 每天下午6点
        id='daily_data_collection_evening',
        name='每日数据采集-下午',
        replace_existing=True,
        max_instances=1,
    )
    
    # 注册Django事件
    register_events(scheduler)
    
    # 注册退出时的清理函数
    atexit.register(lambda: scheduler.shutdown() if scheduler else None)
    
    try:
        logger.info("启动定时任务调度器...")
        scheduler.start()
        logger.info("定时任务调度器启动成功")
        logger.info("已注册定时任务:")
        logger.info("  - 每天凌晨2点: 每日数据采集")
        logger.info("  - 每天上午10点: 每日数据采集")
        logger.info("  - 每天下午6点: 每日数据采集")
    except Exception as e:
        logger.error(f"定时任务调度器启动失败: {str(e)}")
        raise
    
    return scheduler


def stop_scheduler():
    """
    停止定时任务调度器
    """
    global scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown()
        scheduler = None
        logger.info("定时任务调度器已停止")
    else:
        logger.warning("定时任务调度器未运行")
