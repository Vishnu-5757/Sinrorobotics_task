from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer, TaskReportSerializer

class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskUpdateAPIView(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['put']

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskReportAPIView(generics.RetrieveAPIView):
    serializer_class = TaskReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(status='completed')

    def retrieve(self, request, *args, **kwargs):
        if request.user.role not in ['admin', 'superadmin']:
            return Response({"error": "Unauthorized Access"}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)