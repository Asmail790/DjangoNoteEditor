from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.


class Note(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.TextField()

    text = models.TextField()

    def __str__(self) -> str:
        return f"({str(self.title)},{str(self.text)})"


class NoteImage(models.Model):
    image = models.ImageField(upload_to="note_images")
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
