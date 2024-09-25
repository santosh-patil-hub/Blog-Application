from django.urls import path
from .views import register_view, login_view, logout_view,blog_view,profile_view,update_blog,delete_blog,blog_detail_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('',blog_view, name='blog'),  
    path('profile/', profile_view, name='profile'), 
    path('blog/update/<int:blog_id>/', update_blog, name='update_blog'),
    path('blog/delete/<int:blog_id>/', delete_blog, name='delete_blog'),
    path('blog/<int:blog_id>/', blog_detail_view, name='blog_detail'),
]