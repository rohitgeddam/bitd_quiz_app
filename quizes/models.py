from django.db import models

# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    
    created_on = models.DateTimeField(auto_now_add=True)
    roll_out = models.BooleanField(default=False)

