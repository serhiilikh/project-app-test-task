from django.db import models

from projects.models import Project


class Task(models.Model):
    title = models.CharField(max_length=999, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    deadline = models.DateTimeField(blank=False, null=False)
    is_completed = models.BooleanField(default=False, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
