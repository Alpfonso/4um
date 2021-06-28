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
    score = models.IntegerField(default=1)  # stores thread score, used for sorting
    live_thread_content = models.TextField(blank=True)  # live chat stored here
    thread_summary = models.TextField(blank=True)   # contains summary using textrank

    def set_thread_summary(self, ts):
        self.thread_summary = ts

    def set_tags(self, tag_list):
        self.tags = json.dumps(tag_list)    # dump received list in json format

    def get_tags(self):
        return json.loads(self.tags)        # grab tags from list

    def set_lt_content(self, lt_content):
        self.live_thread_content += lt_content + "\n"    # dump received list in json format

    def get_lt_content(self):
        return self.live_thread_content        # grab tags from list

    def set_score(self, score_point):
        self.score += score_point

class Thread_Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=80, blank=False)
    comment_content = models.TextField(max_length=255, blank=False)
    parent_thread = models.ForeignKey(Thread, on_delete=models.CASCADE)