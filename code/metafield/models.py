from django.db import models
from django.utils import timezone

class Metafield(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    key = models.CharField(max_length=64)
    namespace = models.CharField(max_length=255)
    owner_id = models.IntegerField()
    owner_resource = models.CharField(max_length=250)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.TextField()
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.namespace}::{self.key}"

    class Meta:
        unique_together = ('namespace', 'key', 'owner_id', 'owner_resource')