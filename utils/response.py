"""
统一响应格式工具
"""
from rest_framework.response import Response


class ResponseUtil:
    """统一API响应格式"""
    
    @staticmethod
    def success(data=None, msg='操作成功', code=200):
        """
        成功响应
        :param data: 响应数据
        :param msg: 响应消息
        :param code: 响应码
        :return: Response对象
        """
        return Response({
            'code': code,
            'msg': msg,
            'data': data
        })
    
    @staticmethod
    def error(msg='操作失败', code=400, data=None):
        """
        错误响应
        :param msg: 错误消息
        :param code: 错误码
        :param data: 错误数据
        :return: Response对象
        """
        return Response({
            'code': code,
            'msg': msg,
            'data': data
        }, status=code)
    
    @staticmethod
    def paginated_response(queryset, serializer_class, request, msg='查询成功'):
        """
        分页响应
        :param queryset: 查询集
        :param serializer_class: 序列化器类
        :param request: 请求对象
        :param msg: 响应消息
        :return: Response对象
        """
        from rest_framework import viewsets
        from rest_framework.decorators import action
        
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        
        # 手动分页
        from django.core.paginator import Paginator
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = serializer_class(page_obj, many=True)
        
        return Response({
            'code': 200,
            'msg': msg,
            'data': {
                'results': serializer.data,
                'count': paginator.count,
                'page': int(page),
                'page_size': int(page_size),
                'total_pages': paginator.num_pages,
            }
        })

