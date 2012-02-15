from django.db import models

# Create your models here.

class Blogpost(models.Model):
    name = models.CharField(max_length=256, unique=True)
    text = models.TextField()

