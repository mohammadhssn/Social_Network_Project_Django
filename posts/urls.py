from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.all_post, name='all_post'),
    path('post_detail/<int:post_id>/<slug:slug>/', views.post_detail, name='post_detail'),
]