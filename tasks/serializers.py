from rest_framework import serializers

from tasks.models import Task
from projects.models import Project


class CustomTaskSerializer(serializers.ModelSerializer):
    # this serializer is needed to display task data without project id in projects endpoints
    class Meta:
        model = Task
        fields = ["id", "title", "description", "deadline", "is_completed"]
        # this is redundant but explicit
        read_only_fields = ["__all__"]

    def validate(self, data):
        project = data.get("project") or self.instance.project
        if project.deadline < data["deadline"]:
            raise serializers.ValidationError(
                "Task deadline must be less than or equal to a project deadline"
            )
        return data


class TaskSerializer(CustomTaskSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "deadline", "is_completed", "project"]
        read_only_fields = ["id"]
