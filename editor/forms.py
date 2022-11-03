from django.forms import ModelForm
from django import forms
from django.forms import Form
from .models import Note

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title','text']

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)