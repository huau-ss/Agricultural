"""
自定义分页类
"""
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """标准分页类"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """自定义分页响应格式"""
        from rest_framework.response import Response
        return Response({
            'code': 200,
            'msg': '查询成功',
            'data': {
                'results': data,
                'count': self.page.paginator.count,
                'page': self.page.number,
                'page_size': self.page_size,
                'total_pages': self.page.paginator.num_pages,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            }
        })

