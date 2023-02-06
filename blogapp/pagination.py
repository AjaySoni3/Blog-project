from rest_framework.pagination import PageNumberPagination


class blogPagination(PageNumberPagination):

    def get_page_size(self, request):
        return 4
