from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.blog, name='index'),
    path('blog/<int:pk>/', views.blog, name='detail'),
    path('image_upload/', views.image_upload, name='image_upload'),
    path('authorblog/<str:uuid>/', views.author_blog, name='author_blog'),
]