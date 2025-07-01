from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=999, blank=False, null=False)
    deadline = models.DateTimeField(blank=False, null=False)
