from django.db import models

class Notes(models.Model):
    user = models.CharField(max_length=30)
    text_body = models.CharField(max_length=200)
    start_date = models.DateTimeField('Start Date')
    exp_date = models.DateTimeField('Expiration Date')