from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from blogapp.models import Blog
from blogapp.serializers import BlogSerializer, ImageUploadSerializer
from .pagination import blogPagination

# Create your views here.

class BlogAPIView(APIView):

    # pagination_class = blogPagination



    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            query = Blog.objects.get(pk=pk)
            serializer = BlogSerializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        blogs = Blog.objects.all().order_by('-date_posted')
        # page = self.pagination_class()
        # result_page = page.paginate_queryset(blogs, request)
        # serializer = BlogSerializer(result_page, many=True)
        # return page.get_paginated_response(serializer.data)

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        query = Blog.objects.get(pk=pk)
        serializer = BlogSerializer(query, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        pk = request.GET.get('pk')
        query = Blog.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


blog = BlogAPIView.as_view()


class ImageUploadView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            data['image'] = 'http://127.0.0.1:8000' + data['image']
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


image_upload = ImageUploadView.as_view()


class AuthorBlogAPIView(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('uuid')
        if pk:
            query = Blog.objects.filter(author_id=pk)
            serializer = BlogSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


author_blog = AuthorBlogAPIView.as_view()