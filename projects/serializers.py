from rest_framework import serializers

from projects.models import Project
from tasks.serializers import CustomTaskSerializer


class ProjectSerializer(serializers.ModelSerializer):
    tasks = CustomTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "title", "deadline", "tasks"]
        read_only_fields = ["id", "tasks"]
