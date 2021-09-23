from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.all_post, name='all_post'),
    path('post_detail/<int:post_id>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('add_post/<int:user_id>/', views.add_post, name='add_post'),
    path('delete_post/<int:user_id><int:post_id>/', views.delete_post, name='delete_post'),
    path('edit_post/<int:user_id>/<int:post_id>/', views.edit_post, name='edit_post'),
]