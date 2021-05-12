from django.db import models
from django.contrib.auth.models import User

import json


# Create your models here.

class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80, blank=False)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    live_thread = models.BooleanField(default=False)
    sticky_thread = models.BooleanField(default=False)
    tags = models.CharField(default=False, max_length=200)
    score = models.IntegerField(default=1)

    def set_tags(self, tag_list):
        self.tags = json.dumps(tag_list)    # dump received list in json format

    def get_tags(self):
        return json.loads(self.tags)        # grab tags from list

class Thread_Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=80, blank=False)
    comment_content = models.TextField(max_length=255, blank=False)
    parent_thread = models.ForeignKey(Thread, on_delete=models.CASCADE)