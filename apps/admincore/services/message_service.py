"""
消息通知服务
"""
import logging
from django.utils import timezone
from django.contrib.auth.models import User
from apps.admincore.models import UserMessage, SystemAnnouncement, PriceAlert

logger = logging.getLogger(__name__)


class MessageService:
    """消息服务类"""
    
    @staticmethod
    def send_system_message(user, title, content, message_type='system', related_alert=None):
        """
        发送站内信
        :param user: 接收用户
        :param title: 标题
        :param content: 内容
        :param message_type: 消息类型
        :param related_alert: 关联预警
        :return: 消息对象
        """
        try:
            message = UserMessage.objects.create(
                user=user,
                title=title,
                content=content,
                message_type=message_type,
                related_alert=related_alert
            )
            logger.info(f"发送站内信给用户 {user.username}: {title}")
            return message
        except Exception as e:
            logger.error(f"发送站内信失败: {str(e)}")
            return None
    
    @staticmethod
    def send_bulk_message(users, title, content, message_type='system'):
        """
        批量发送站内信
        :param users: 用户列表或QuerySet
        :param title: 标题
        :param content: 内容
        :param message_type: 消息类型
        :return: 创建的消息数量
        """
        try:
            messages = []
            for user in users:
                message = UserMessage(
                    user=user,
                    title=title,
                    content=content,
                    message_type=message_type
                )
                messages.append(message)
            
            UserMessage.objects.bulk_create(messages)
            logger.info(f"批量发送站内信给 {len(messages)} 个用户: {title}")
            return len(messages)
        except Exception as e:
            logger.error(f"批量发送站内信失败: {str(e)}")
            return 0
    
    @staticmethod
    def send_alert_notification(alert, users=None):
        """
        发送预警通知
        :param alert: 预警对象
        :param users: 指定用户列表，如果为None则发送给所有订阅用户
        :return: 发送的消息数量
        """
        try:
            if users is None:
                # 从预警关联的订阅中获取用户
                from apps.admincore.models import UserAlertSubscription
                subscriptions = UserAlertSubscription.objects.filter(
                    is_active=True,
                    alert_type=alert.alert_type,
                    product_name=alert.product_name if alert.product_name else None,
                    region=alert.region if alert.region else None
                )
                users = [sub.user for sub in subscriptions]
            
            count = MessageService.send_bulk_message(
                users,
                f"价格预警：{alert.product_name}",
                alert.message,
                message_type='alert'
            )
            
            return count
        except Exception as e:
            logger.error(f"发送预警通知失败: {str(e)}")
            return 0
    
    @staticmethod
    def create_announcement(title, content, announcement_type='system', priority='normal', 
                          created_by=None, publish_now=False):
        """
        创建系统公告
        :param title: 标题
        :param content: 内容
        :param announcement_type: 公告类型
        :param priority: 优先级
        :param created_by: 创建人
        :param publish_now: 是否立即发布
        :return: 公告对象
        """
        try:
            announcement = SystemAnnouncement.objects.create(
                title=title,
                content=content,
                announcement_type=announcement_type,
                priority=priority,
                created_by=created_by,
                is_published=publish_now,
                publish_at=timezone.now() if publish_now else None
            )
            logger.info(f"创建系统公告: {title}")
            return announcement
        except Exception as e:
            logger.error(f"创建系统公告失败: {str(e)}")
            return None
    
    @staticmethod
    def get_unread_count(user):
        """
        获取用户未读消息数量
        :param user: 用户对象
        :return: 未读数量
        """
        return UserMessage.objects.filter(user=user, is_read=False).count()
    
    @staticmethod
    def mark_as_read(message_id, user):
        """
        标记消息为已读
        :param message_id: 消息ID
        :param user: 用户对象
        :return: 是否成功
        """
        try:
            message = UserMessage.objects.get(id=message_id, user=user)
            if not message.is_read:
                message.is_read = True
                message.read_at = timezone.now()
                message.save()
            return True
        except UserMessage.DoesNotExist:
            return False
    
    @staticmethod
    def mark_all_as_read(user):
        """
        标记所有消息为已读
        :param user: 用户对象
        :return: 更新的消息数量
        """
        try:
            count = UserMessage.objects.filter(
                user=user,
                is_read=False
            ).update(
                is_read=True,
                read_at=timezone.now()
            )
            return count
        except Exception as e:
            logger.error(f"标记所有消息为已读失败: {str(e)}")
            return 0

