from django.forms import ModelForm
from django import forms
from django.forms import Form
from .models import Note

class NoteForm(ModelForm):
    
    class Meta:
        
        model = Note
        
        fields = ['title','text']



class LoginForm(forms.Form):
    
    username = forms.CharField(label='username', max_length=100)

    password = forms.CharField(widget=forms.PasswordInput, max_length=100)
