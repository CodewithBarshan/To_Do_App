from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) #User model will do everything for us #one to many relationship
    title=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    complete=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)#whenever we create a new task in the list,automativally it will catch the time of creation


    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['complete'] #means completed task will shown later
