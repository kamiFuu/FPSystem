from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # URL cho trang chủ của ứng dụng ProjectManager
    path('', views.home, name='projectmanager_home'),
    # Các URL khác cho các chức năng như quản lý dự án, tạo dự án mới, v.v.
    path('manage/', views.project_list, name='manage_projects'),
    path('create/', views.create_project, name='create_project'),
    path('detail/<int:project_id>/', views.project_detail, name='project_detail'),
   
]
