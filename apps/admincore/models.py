"""
系统管理模块 - 数据模型
"""
from django.db import models
from django.contrib.auth.models import User


class SystemLog(models.Model):
    """系统日志"""
    log_type = models.CharField(
        max_length=50,
        choices=[
            ('info', '信息'),
            ('warning', '警告'),
            ('error', '错误'),
            ('debug', '调试'),
        ],
        verbose_name='日志类型'
    )
    module = models.CharField(max_length=100, verbose_name='模块')
    action = models.CharField(max_length=100, verbose_name='操作')
    message = models.TextField(verbose_name='日志内容')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='用户'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'system_log'
        verbose_name = '系统日志'
        verbose_name_plural = '系统日志'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['log_type', 'created_at']),
            models.Index(fields=['module', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.log_type} - {self.module} - {self.created_at}"


class PriceAlert(models.Model):
    """价格预警"""
    product_name = models.CharField(max_length=100, verbose_name='农产品名称')
    region = models.CharField(max_length=50, verbose_name='地区')
    alert_type = models.CharField(
        max_length=50,
        choices=[
            ('price_rise', '价格上涨'),
            ('price_fall', '价格下跌'),
            ('price_abnormal', '价格异常'),
        ],
        verbose_name='预警类型'
    )
    threshold = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='阈值')
    current_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='当前价格')
    change_rate = models.FloatField(verbose_name='变化率(%)')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待处理'),
            ('processed', '已处理'),
            ('ignored', '已忽略'),
        ],
        default='pending',
        verbose_name='状态'
    )
    message = models.TextField(verbose_name='预警信息')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name='处理时间')
    
    class Meta:
        db_table = 'price_alert'
        verbose_name = '价格预警'
        verbose_name_plural = '价格预警'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product_name', 'status']),
            models.Index(fields=['alert_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.product_name} - {self.alert_type} - {self.created_at}"


class AlertRule(models.Model):
    """预警规则配置"""
    rule_name = models.CharField(max_length=100, verbose_name='规则名称')
    product_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='农产品名称')
    region = models.CharField(max_length=50, null=True, blank=True, verbose_name='地区')
    alert_type = models.CharField(
        max_length=50,
        choices=[
            ('price_rise', '价格上涨'),
            ('price_fall', '价格下跌'),
            ('price_abnormal', '价格异常'),
        ],
        verbose_name='预警类型'
    )
    threshold_type = models.CharField(
        max_length=50,
        choices=[
            ('absolute', '绝对值'),
            ('percentage', '百分比'),
        ],
        verbose_name='阈值类型'
    )
    threshold_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='阈值')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'alert_rule'
        verbose_name = '预警规则'
        verbose_name_plural = '预警规则'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.rule_name} - {self.alert_type}"


class UserPermission(models.Model):
    """用户权限扩展"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    role = models.CharField(
        max_length=50,
        choices=[
            ('admin', '管理员'),
            ('analyst', '分析师'),
            ('trader', '交易员'),
            ('viewer', '查看者'),
        ],
        default='viewer',
        verbose_name='角色'
    )
    permissions = models.JSONField(default=dict, verbose_name='权限配置')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user_permission'
        verbose_name = '用户权限'
        verbose_name_plural = '用户权限'
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


class SystemAnnouncement(models.Model):
    """系统公告"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    announcement_type = models.CharField(
        max_length=50,
        choices=[
            ('system', '系统公告'),
            ('maintenance', '维护公告'),
            ('update', '更新公告'),
            ('other', '其他'),
        ],
        default='system',
        verbose_name='公告类型'
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', '低'),
            ('normal', '普通'),
            ('high', '高'),
            ('urgent', '紧急'),
        ],
        default='normal',
        verbose_name='优先级'
    )
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    publish_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    expire_at = models.DateTimeField(null=True, blank=True, verbose_name='过期时间')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_announcements',
        verbose_name='创建人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'system_announcement'
        verbose_name = '系统公告'
        verbose_name_plural = '系统公告'
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['is_published', 'publish_at']),
            models.Index(fields=['announcement_type', 'is_published']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.announcement_type}"


class UserMessage(models.Model):
    """站内信"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='接收用户'
    )
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    message_type = models.CharField(
        max_length=50,
        choices=[
            ('alert', '预警通知'),
            ('system', '系统通知'),
            ('trade', '交易通知'),
            ('other', '其他'),
        ],
        default='system',
        verbose_name='消息类型'
    )
    related_alert = models.ForeignKey(
        PriceAlert,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
        verbose_name='关联预警'
    )
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='阅读时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'user_message'
        verbose_name = '站内信'
        verbose_name_plural = '站内信'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['message_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class UserAlertSubscription(models.Model):
    """用户预警订阅"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='alert_subscriptions',
        verbose_name='用户'
    )
    product_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='农产品名称')
    region = models.CharField(max_length=50, null=True, blank=True, verbose_name='地区')
    alert_type = models.CharField(
        max_length=50,
        choices=[
            ('price_rise', '价格上涨'),
            ('price_fall', '价格下跌'),
            ('price_abnormal', '价格异常'),
        ],
        verbose_name='预警类型'
    )
    threshold_type = models.CharField(
        max_length=50,
        choices=[
            ('absolute', '绝对值'),
            ('percentage', '百分比'),
        ],
        verbose_name='阈值类型'
    )
    threshold_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='阈值')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user_alert_subscription'
        verbose_name = '用户预警订阅'
        verbose_name_plural = '用户预警订阅'
        ordering = ['-created_at']
        unique_together = [['user', 'product_name', 'region', 'alert_type']]
    
    def __str__(self):
        return f"{self.user.username} - {self.product_name} - {self.alert_type}"

