from django.contrib import admin
from . models import Task

# Register your models here.
# to see created model into database we have register it into admin,py
admin.site.register(Task)
