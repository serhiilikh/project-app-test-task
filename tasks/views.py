from rest_framework import viewsets

from tasks.serializers import TaskSerializer
from tasks.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("id").select_related("project")
    serializer_class = TaskSerializer
