from django.db import models

# Create your models here.

class Thread(models.Model):
    title = models.CharField(max_length=80, blank=False)
    description = models.TextField(blank=True)
    user = models.CharField(max_length=20)
    live_thread = models.BooleanField(default=False)
    sticky_thread = models.BooleanField(default=False)