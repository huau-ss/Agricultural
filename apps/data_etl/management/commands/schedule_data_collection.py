"""
定时数据采集命令
可以手动执行或通过cron定时执行
用法: python manage.py schedule_data_collection --source-id 1
"""
from django.core.management.base import BaseCommand
from apps.data_etl.tasks import daily_data_collection_task


class Command(BaseCommand):
    help = '执行定时数据采集任务'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--source-id',
            type=int,
            default=None,
            help='数据源ID（可选，不指定则采集所有启用的数据源）'
        )
        parser.add_argument(
            '--time',
            type=str,
            default=None,
            help='指定采集时间（格式：HH:MM，例如：02:00）'
        )
    
    def handle(self, *args, **options):
        source_id = options.get('source_id')
        
        self.stdout.write('=' * 60)
        self.stdout.write('开始执行定时数据采集任务')
        self.stdout.write('=' * 60)
        
        if source_id:
            self.stdout.write(f'数据源ID: {source_id}')
        else:
            self.stdout.write('采集所有启用的数据源')
        
        try:
            result = daily_data_collection_task(source_id=source_id)
            
            if result['success']:
                self.stdout.write(self.style.SUCCESS(f"\n✓ {result['message']}"))
                self.stdout.write(f"\n执行时间: {result['timestamp']}")
                self.stdout.write(f"\n任务详情:")
                self.stdout.write('-' * 60)
                
                for task_info in result['tasks']:
                    if task_info.get('status') == 'failed':
                        self.stdout.write(self.style.ERROR(
                            f"✗ {task_info['source_name']}: {task_info.get('error', '未知错误')}"
                        ))
                    else:
                        self.stdout.write(
                            f"✓ {task_info['source_name']}:\n"
                            f"  任务: {task_info.get('task_name', 'N/A')}\n"
                            f"  状态: {task_info.get('status', 'N/A')}\n"
                            f"  总数: {task_info.get('total_count', 0)}\n"
                            f"  成功: {task_info.get('success_count', 0)}\n"
                            f"  失败: {task_info.get('failed_count', 0)}\n"
                        )
                
                self.stdout.write('-' * 60)
                self.stdout.write(self.style.SUCCESS('\n定时数据采集任务完成！'))
            else:
                self.stdout.write(self.style.ERROR(f"\n✗ {result['message']}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n定时数据采集任务失败: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())

