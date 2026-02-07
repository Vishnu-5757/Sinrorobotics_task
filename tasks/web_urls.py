from django.urls import path
from . import web_views

urlpatterns = [
    path('', web_views.dashboard, name='dashboard'),
    path('logout/', web_views.logout_view, name='logout'),
    path('manage-users/', web_views.manage_users, name='manage_users'),
    path('task/<int:pk>/', web_views.task_detail, name='task_detail'),


    path('manage-users/create/', web_views.user_create, name='user_create'),
    path('manage-users/delete/<int:pk>/', web_views.user_delete, name='user_delete'),
    path('manage-users/update/<int:pk>/', web_views.user_update, name='user_update'),


    path('manage-tasks/', web_views.manage_tasks, name='manage_tasks'),
    path('manage-tasks/create/', web_views.task_upsert, name='task_create'),
    path('manage-tasks/update/<int:pk>/', web_views.task_upsert, name='task_update'),
    path('manage-tasks/delete/<int:pk>/', web_views.task_delete, name='task_delete'),

    path('reports/', web_views.task_reports, name='task_reports'),
]