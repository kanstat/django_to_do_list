from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    # we a task to be owened by specific user so import builtin django modle
    # to set the values we create one to on relationship (one-to-many) i.ie one user can havr many items
    # can be set with foreginkey value, on_delete---> what we do the task if user gets deleted(in this case i
    # want if user gets deleted all the child tasks deleted)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# i want to set the default ordering so i will just set some metadata here,
# we want to order the model by complete status so any complete item should be send to the bottem of list
# this is how we can order query set whenever we returning multiple items we can order it by title, user etc.


class Meta:
    ordering = ['complete']
