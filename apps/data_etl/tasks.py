"""
定时任务 - 数据采集任务
"""
import logging
from datetime import datetime
from django.utils import timezone
from apps.data_etl.services import ETLService
from apps.data_etl.models import DataSource, ETLTask

logger = logging.getLogger(__name__)


def daily_data_collection_task(source_id=None):
    """
    每日数据采集任务
    :param source_id: 数据源ID，如果为None则采集所有启用的数据源
    :return: 任务结果
    """
    try:
        etl_service = ETLService()
        results = []
        
        if source_id:
            # 采集指定数据源
            sources = DataSource.objects.filter(id=source_id, status='active')
        else:
            # 采集所有启用的数据源
            sources = DataSource.objects.filter(status='active')
        
        if not sources.exists():
            logger.warning("没有找到启用的数据源")
            return {
                'success': False,
                'message': '没有找到启用的数据源',
                'tasks': []
            }
        
        for source in sources:
            try:
                task_name = f"定时采集-{source.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                logger.info(f"开始执行定时采集任务: {task_name}, 数据源: {source.name}")
                
                task = etl_service.run_etl_task(source_id=source.id, task_name=task_name)
                
                results.append({
                    'source_id': source.id,
                    'source_name': source.name,
                    'task_id': task.id,
                    'task_name': task.task_name,
                    'status': task.status,
                    'total_count': task.total_count,
                    'success_count': task.success_count,
                    'failed_count': task.failed_count,
                })
                
                logger.info(
                    f"定时采集任务完成: {task_name}, "
                    f"成功: {task.success_count}, 失败: {task.failed_count}"
                )
                
            except Exception as e:
                logger.error(f"数据源 {source.name} 采集失败: {str(e)}")
                results.append({
                    'source_id': source.id,
                    'source_name': source.name,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return {
            'success': True,
            'message': f'完成 {len(results)} 个数据源的采集',
            'tasks': results,
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"定时采集任务执行失败: {str(e)}")
        return {
            'success': False,
            'message': f'任务执行失败: {str(e)}',
            'tasks': [],
            'timestamp': timezone.now().isoformat()
        }


def scheduled_data_collection():
    """
    定时数据采集（默认采集所有启用的数据源）
    """
    return daily_data_collection_task()

