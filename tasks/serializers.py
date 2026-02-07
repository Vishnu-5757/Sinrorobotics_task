from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        if data.get('status') == 'completed':
            if not data.get('completion_report'):
                raise serializers.ValidationError({"completion_report": "This field is required when completing a task."})
            if not data.get('worked_hours') or data.get('worked_hours') <= 0:
                raise serializers.ValidationError({"worked_hours": "Valid worked hours are required when completing a task."})
        return data

class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'completion_report', 'worked_hours']