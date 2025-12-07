"""
快速运行爬虫测试脚本
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agricultural_platform.settings')
django.setup()

from apps.data_etl.models import DataSource
from apps.data_etl.services import ETLService

def main():
    print("=" * 50)
    print("开始运行爬虫测试")
    print("=" * 50)
    
    # 1. 创建或获取数据源
    print("\n1. 检查数据源...")
    source, created = DataSource.objects.get_or_create(
        name="全国农产品批发市场价格",
        defaults={
            'url': 'https://pfsc.agri.cn/#/priceMarket',
            'source_type': 'web',
            'status': 'active'
        }
    )
    
    if created:
        print(f"✓ 创建新数据源，ID: {source.id}")
    else:
        print(f"✓ 使用现有数据源，ID: {source.id}")
    
    # 2. 运行爬虫
    print(f"\n2. 启动爬虫（数据源ID: {source.id}）...")
    try:
        etl_service = ETLService()
        task = etl_service.run_etl_task(
            source_id=source.id,
            task_name=f"测试爬虫-{source.name}"
        )
        
        print("\n" + "=" * 50)
        print("爬虫执行完成！")
        print("=" * 50)
        print(f"任务名称: {task.task_name}")
        print(f"状态: {task.status}")
        print(f"总记录数: {task.total_count}")
        print(f"成功数: {task.success_count}")
        print(f"失败数: {task.failed_count}")
        
        if task.failed_count > 0:
            print(f"\n警告: 有 {task.failed_count} 条数据清洗失败")
        
        # 3. 查看结果
        print("\n3. 数据查看地址:")
        print(f"   - 原始数据: http://127.0.0.1:8000/api/data-etl/raw-data/")
        print(f"   - 清洗数据: http://127.0.0.1:8000/api/data-etl/cleaned-data/")
        print(f"   - 市场价格: http://127.0.0.1:8000/api/market/prices/")
        print(f"   - Admin后台: http://127.0.0.1:8000/admin/")
        
    except Exception as e:
        print(f"\n✗ 爬虫执行失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

