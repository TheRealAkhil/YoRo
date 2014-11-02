from django.db import models

class Note(models.Model):
    user = models.CharField(max_length=30)
    text_body = models.CharField(max_length=200)
    time = models.DateTimeField('Reminder Date')
    flag = models.BooleanField(default=False)