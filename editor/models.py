from django.db import models
# Create your models here.

class Note(models.Model):
    title = models.TextField()
    text = models.TextField()

    def __str__(self) -> str:
        return f"({str(self.title)},{str(self.text)})"

