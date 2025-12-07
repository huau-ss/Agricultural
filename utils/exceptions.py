"""
自定义异常类
"""
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from utils.response import ResponseUtil


class BusinessException(APIException):
    """业务异常"""
    status_code = 400
    default_detail = '业务处理失败'
    default_code = 'business_error'


class DataException(APIException):
    """数据异常"""
    status_code = 400
    default_detail = '数据错误'
    default_code = 'data_error'


def custom_exception_handler(exc, context):
    """
    自定义异常处理器
    :param exc: 异常对象
    :param context: 上下文
    :return: Response对象
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'code': response.status_code,
            'msg': str(exc.detail) if hasattr(exc, 'detail') else str(exc),
            'data': None
        }
        response.data = custom_response_data
    
    return response

