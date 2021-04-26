from django.contrib import admin

# Register your models here.
from .models import Thread, Thread_Comment

admin.site.register(Thread)
admin.site.register(Thread_Comment)
