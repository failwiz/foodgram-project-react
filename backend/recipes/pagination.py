from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """Переопределение класса пагинации, для изменения лимита отображения."""
    page_size_query_param = 'limit'
