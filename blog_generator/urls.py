from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('generate_blog', views.generate_blog, name='generate-blog'),
    path('blog-list', views.blog-list, name='blog-list'),
    path('blog-details/<int:pk>/', views.blog-details, name='blog-details'),
]


