from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.post_create, name='create_post'),
    path('like/', views.like_post, name='like'),
]
