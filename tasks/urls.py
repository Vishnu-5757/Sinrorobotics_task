from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskListAPIView, TaskUpdateAPIView, TaskReportAPIView

urlpatterns = [
    # User Authentication (JWT)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Task Endpoints
    path('tasks/', TaskListAPIView.as_view(), name='api_task_list'),
    path('tasks/<int:pk>/', TaskUpdateAPIView.as_view(), name='api_task_update'),
    path('tasks/<int:pk>/report/', TaskReportAPIView.as_view(), name='api_task_report'),
]