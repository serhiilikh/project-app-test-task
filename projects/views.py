from rest_framework import viewsets

from projects.serializers import ProjectSerializer
from projects.models import Project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("id").prefetch_related("tasks")
    serializer_class = ProjectSerializer
