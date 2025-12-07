"""
定时检查预警命令
可以通过cron或celery定时执行
"""
from django.core.management.base import BaseCommand
from apps.admincore.services import AlertService


class Command(BaseCommand):
    help = '检查价格预警并生成预警信息'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['forecast', 'price', 'all'],
            default='all',
            help='预警检查类型：forecast(预测预警), price(价格变化预警), all(全部)'
        )
    
    def handle(self, *args, **options):
        check_type = options['type']
        
        if check_type in ['forecast', 'all']:
            self.stdout.write('开始检查预测预警...')
            count = AlertService.check_forecast_alerts()
            self.stdout.write(self.style.SUCCESS(f'预测预警检查完成，创建 {count} 个预警'))
        
        if check_type in ['price', 'all']:
            self.stdout.write('开始检查价格变化预警...')
            count = AlertService.check_price_change_alerts()
            self.stdout.write(self.style.SUCCESS(f'价格变化预警检查完成，创建 {count} 个预警'))
        
        self.stdout.write(self.style.SUCCESS('预警检查任务完成'))

