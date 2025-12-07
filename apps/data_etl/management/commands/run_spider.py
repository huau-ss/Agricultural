"""
运行爬虫命令
用法: python manage.py run_spider --source-id 1
"""
from django.core.management.base import BaseCommand
from apps.data_etl.services import ETLService


class Command(BaseCommand):
    help = '运行数据采集爬虫'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--source-id',
            type=int,
            required=True,
            help='数据源ID'
        )
        parser.add_argument(
            '--task-name',
            type=str,
            default=None,
            help='任务名称（可选）'
        )
    
    def handle(self, *args, **options):
        source_id = options['source_id']
        task_name = options.get('task_name')
        
        self.stdout.write(f'开始执行ETL任务，数据源ID: {source_id}')
        
        try:
            etl_service = ETLService()
            task = etl_service.run_etl_task(source_id=source_id, task_name=task_name)
            
            self.stdout.write(self.style.SUCCESS(
                f'ETL任务完成！\n'
                f'任务名称: {task.task_name}\n'
                f'状态: {task.status}\n'
                f'总记录数: {task.total_count}\n'
                f'成功: {task.success_count}\n'
                f'失败: {task.failed_count}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'ETL任务失败: {str(e)}'))

