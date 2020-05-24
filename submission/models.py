from django.db import models

class submissions(models.Model):
    name = models.CharField(max_length=255)
    id = models.CharField(max_length=10,primary_key=True)
    file = models.ImageField(upload_to="submissions")