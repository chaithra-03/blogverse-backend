from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name= 'register_user'),
    path('create_blog/', views.create_blog, name='create-blog'),
    path('blog_list/', views.blog_list, name='blog-list'),
    path('blogs/<slug:slug>', views.get_blog, name = 'get_blog'),
    path('update_blog/<int:pk>/', views.update_blog, name='update-blog'),
    path('delete_blog/<int:pk>/', views.delete_blog, name='delete-blog'),
    path('update_user/', views.update_user_profile, name='update-user'),
    path('get_username/', views.get_username, name = 'get_username'),
    path("get_userinfo/<str:username>", views.get_userinfo, name="get_userinfo"),

]