from django.contrib import admin
from .models import Note
from .models import NoteImage

admin.site.register(Note)
admin.site.register(NoteImage)
# Register your models here.
