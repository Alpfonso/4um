from django.db import models

# Create your models here.

class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80, blank=False)
    description = models.TextField(blank=True)
    user = models.CharField(max_length=100)
    live_thread = models.BooleanField(default=False)
    sticky_thread = models.BooleanField(default=False)

class Thread_Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=80, blank=False)
    comment_content = models.TextField(max_length=255, blank=False)
    parent_thread = models.ForeignKey(Thread, on_delete=models.CASCADE)