from datetime import timezone
from django.contrib.auth.models import update_last_login
from django.db import models
import django.utils.timezone
import json

# Create your models here.
class Profile(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    profile_description = models.TextField(max_length=255, default="Enter short profile description")
    vote_amount = models.IntegerField(default=100)
    common_user_tags = models.CharField(default='["none"]', max_length=200)
    user_tag_collection = models.TextField(default='["none"]')
    last_online = models.DateField(default=django.utils.timezone.datetime.now)

    def set_vote_points(self, vote):
        self.vote_amount -= vote

    def reset_votes(self):
        self.vote_amount = 100

    def set_tags(self, tag_list):
        check = self.get_tags()
        print(check)
        print(type(check))
        if  'none' in check:
            self.user_tag_collection = json.dumps(tag_list)
            self.common_user_tags = json.dumps(tag_list)    # dump received list in json format
        else:
            tag_join = self.get_tags_collection() + tag_list
            self.user_tag_collection = json.dumps(tag_join)
            print(tag_join)
            result_tags = sorted(set(tag_join), key = lambda ele: tag_join.count(ele), reverse=True)
            shortened_list = result_tags[:5]
            self.common_user_tags = json.dumps(shortened_list)

    def get_tags(self):
        #if self.common_user_tags != 'False':
            return json.loads(self.common_user_tags)        # grab tags from list
        #else:
            #print("Empty variable")
            #return False
    
    def get_tags_collection(self):
        #if self.user_tag_collection != 'False':
            return json.loads(self.user_tag_collection)        # grab tags from list
        #else:
            #print("Empty variable")
            #return False

    def set_last_login(self):
        self.last_online = str(django.utils.timezone.datetime.now().date())