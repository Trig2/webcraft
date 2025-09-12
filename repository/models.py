from django.db import models
from projects.models import Project


# Create your models here.
class Repository(models.Model):
    repository_name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    repository_link = models.URLField(max_length=200)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.repository_link
