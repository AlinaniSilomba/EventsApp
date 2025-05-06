from django.db import models
from django.contrib.auth.models import User

class EventModel(models.Model):
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    event_day = models.DateField(null=False, blank=False )
    time = models.TimeField(auto_now=True,)
    description = models.TextField(max_length=100)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return f'{self.author} {self.description} {self.created_at}'
