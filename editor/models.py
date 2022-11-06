from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Note(models.Model):
    
    user = models.ForeignKey(User, on_delete =  models.CASCADE)
    
    title = models.TextField()
    
    text = models.TextField()

    def __str__(self) -> str:
        return f"({str(self.title)},{str(self.text)})"

