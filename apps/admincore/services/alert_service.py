"""
智能预警服务
"""
import logging
from decimal import Decimal
from django.utils import timezone
from django.db.models import Q
from apps.admincore.models import PriceAlert, AlertRule, UserAlertSubscription, UserMessage
from apps.forecast.models import ForecastResult
from apps.market.models import MarketPrice

logger = logging.getLogger(__name__)


class AlertService:
    """预警服务类"""
    
    @staticmethod
    def check_forecast_alerts():
        """
        检查预测结果并生成预警
        当预测价格变化超过阈值时，自动生成预警
        """
        try:
            # 获取所有启用的预警规则
            rules = AlertRule.objects.filter(is_active=True)
            
            alerts_created = 0
            
            for rule in rules:
                # 获取最新的预测结果
                forecast_query = ForecastResult.objects.filter(
                    product_name=rule.product_name if rule.product_name else None,
                    region=rule.region if rule.region else None,
                    forecast_date__gte=timezone.now().date()
                ).order_by('-forecast_date')
                
                if not forecast_query.exists():
                    continue
                
                latest_forecast = forecast_query.first()
                
                # 获取当前市场价格
                current_price_query = MarketPrice.objects.filter(
                    product_name=latest_forecast.product_name,
                    region=latest_forecast.region
                ).order_by('-date')
                
                if not current_price_query.exists():
                    continue
                
                current_price = current_price_query.first().price
                forecast_price = latest_forecast.forecast_price
                
                # 计算价格变化
                price_change = float(forecast_price) - float(current_price)
                
                if rule.threshold_type == 'percentage':
                    change_rate = (price_change / float(current_price)) * 100 if current_price > 0 else 0
                    threshold_value = float(rule.threshold_value)
                else:
                    change_rate = price_change
                    threshold_value = float(rule.threshold_value)
                
                # 判断是否触发预警
                should_alert = False
                alert_type = None
                
                if rule.alert_type == 'price_rise' and change_rate > threshold_value:
                    should_alert = True
                    alert_type = 'price_rise'
                elif rule.alert_type == 'price_fall' and change_rate < -threshold_value:
                    should_alert = True
                    alert_type = 'price_fall'
                elif rule.alert_type == 'price_abnormal' and abs(change_rate) > threshold_value:
                    should_alert = True
                    alert_type = 'price_abnormal'
                
                if should_alert:
                    # 检查是否已存在相同预警（避免重复）
                    existing_alert = PriceAlert.objects.filter(
                        product_name=latest_forecast.product_name,
                        region=latest_forecast.region,
                        alert_type=alert_type,
                        status='pending',
                        created_at__gte=timezone.now() - timezone.timedelta(hours=24)
                    ).first()
                    
                    if not existing_alert:
                        # 创建预警
                        message = AlertService._generate_alert_message(
                            latest_forecast.product_name,
                            latest_forecast.region,
                            alert_type,
                            current_price,
                            forecast_price,
                            change_rate
                        )
                        
                        alert = PriceAlert.objects.create(
                            product_name=latest_forecast.product_name,
                            region=latest_forecast.region,
                            alert_type=alert_type,
                            threshold=rule.threshold_value,
                            current_price=current_price,
                            change_rate=change_rate,
                            message=message,
                            status='pending'
                        )
                        
                        alerts_created += 1
                        
                        # 发送站内信给订阅用户
                        AlertService._notify_subscribed_users(alert)
                        
                        logger.info(f"创建预警: {alert.product_name} - {alert.alert_type}")
            
            logger.info(f"预警检查完成，创建 {alerts_created} 个预警")
            return alerts_created
            
        except Exception as e:
            logger.error(f"预警检查失败: {str(e)}")
            return 0
    
    @staticmethod
    def _generate_alert_message(product_name, region, alert_type, current_price, forecast_price, change_rate):
        """
        生成预警消息
        """
        alert_type_map = {
            'price_rise': '价格上涨',
            'price_fall': '价格下跌',
            'price_abnormal': '价格异常波动'
        }
        
        message = f"【价格预警】{product_name}（{region}）预计将出现{alert_type_map.get(alert_type, '异常')}。"
        message += f"当前价格：{current_price}元，预测价格：{forecast_price}元，"
        message += f"预计变化率：{change_rate:.2f}%。请及时关注市场动态，做好应对准备。"
        
        return message
    
    @staticmethod
    def _notify_subscribed_users(alert):
        """
        通知订阅用户
        """
        try:
            # 查找订阅了该预警的用户
            subscriptions = UserAlertSubscription.objects.filter(
                is_active=True,
                alert_type=alert.alert_type
            )
            
            # 根据产品名称和地区过滤
            if alert.product_name:
                subscriptions = subscriptions.filter(
                    Q(product_name=alert.product_name) | Q(product_name__isnull=True)
                )
            if alert.region:
                subscriptions = subscriptions.filter(
                    Q(region=alert.region) | Q(region__isnull=True)
                )
            
            # 检查阈值是否匹配
            for subscription in subscriptions:
                if subscription.threshold_type == 'percentage':
                    threshold = float(subscription.threshold_value)
                    if abs(alert.change_rate) >= threshold:
                        # 创建站内信
                        UserMessage.objects.create(
                            user=subscription.user,
                            title=f"价格预警：{alert.product_name}",
                            content=alert.message,
                            message_type='alert',
                            related_alert=alert
                        )
                else:
                    threshold = float(subscription.threshold_value)
                    price_change = abs(float(alert.current_price) * (alert.change_rate / 100))
                    if price_change >= threshold:
                        # 创建站内信
                        UserMessage.objects.create(
                            user=subscription.user,
                            title=f"价格预警：{alert.product_name}",
                            content=alert.message,
                            message_type='alert',
                            related_alert=alert
                        )
            
        except Exception as e:
            logger.error(f"通知订阅用户失败: {str(e)}")
    
    @staticmethod
    def check_price_change_alerts():
        """
        检查市场价格变化并生成预警（基于实际价格变化）
        """
        try:
            rules = AlertRule.objects.filter(is_active=True)
            alerts_created = 0
            
            for rule in rules:
                # 获取最近两天的价格数据
                recent_prices = MarketPrice.objects.filter(
                    product_name=rule.product_name if rule.product_name else None,
                    region=rule.region if rule.region else None
                ).order_by('-date')[:2]
                
                if len(recent_prices) < 2:
                    continue
                
                current_price = recent_prices[0].price
                previous_price = recent_prices[1].price
                
                # 计算价格变化
                price_change = float(current_price) - float(previous_price)
                
                if rule.threshold_type == 'percentage':
                    change_rate = (price_change / float(previous_price)) * 100 if previous_price > 0 else 0
                    threshold_value = float(rule.threshold_value)
                else:
                    change_rate = price_change
                    threshold_value = float(rule.threshold_value)
                
                # 判断是否触发预警
                should_alert = False
                alert_type = None
                
                if rule.alert_type == 'price_rise' and change_rate > threshold_value:
                    should_alert = True
                    alert_type = 'price_rise'
                elif rule.alert_type == 'price_fall' and change_rate < -threshold_value:
                    should_alert = True
                    alert_type = 'price_fall'
                elif rule.alert_type == 'price_abnormal' and abs(change_rate) > threshold_value:
                    should_alert = True
                    alert_type = 'price_abnormal'
                
                if should_alert:
                    # 检查是否已存在相同预警
                    existing_alert = PriceAlert.objects.filter(
                        product_name=recent_prices[0].product_name,
                        region=recent_prices[0].region,
                        alert_type=alert_type,
                        status='pending',
                        created_at__gte=timezone.now() - timezone.timedelta(hours=24)
                    ).first()
                    
                    if not existing_alert:
                        message = AlertService._generate_alert_message(
                            recent_prices[0].product_name,
                            recent_prices[0].region,
                            alert_type,
                            previous_price,
                            current_price,
                            change_rate
                        )
                        
                        alert = PriceAlert.objects.create(
                            product_name=recent_prices[0].product_name,
                            region=recent_prices[0].region,
                            alert_type=alert_type,
                            threshold=rule.threshold_value,
                            current_price=current_price,
                            change_rate=change_rate,
                            message=message,
                            status='pending'
                        )
                        
                        alerts_created += 1
                        AlertService._notify_subscribed_users(alert)
            
            return alerts_created
            
        except Exception as e:
            logger.error(f"价格变化预警检查失败: {str(e)}")
            return 0

