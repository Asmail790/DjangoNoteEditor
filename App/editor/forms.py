from django.forms import inlineformset_factory
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm, ValidationError
from django import forms
from django.forms import Form
from .models import Note, NoteImage

from django.contrib.auth.models import User
from . utilities import get_field

MAX_PASSWORD_LENGTH = get_field('password', User).max_length
MAX_USERNAME_LENGTH = get_field('username', User).max_length


class NoteForm(ModelForm):

    class Meta:

        model = Note

        fields = ['title', 'text']


class LoginForm(forms.Form):
    # TODO  implement  Widget.render() or  template_render to work with bootstrap 
    username = forms.CharField(label='username', max_length=100)


    password = forms.CharField(widget=forms.PasswordInput, max_length=100)

    username.widget.attrs.update({'class': 'form-control input-group mb-2'})
    password.widget.attrs.update({'class': 'form-control input-group mb-2'})

class RegisterForm(forms.Form):

    username = forms.CharField(label='username', max_length=100)

    password = forms.CharField(
        label="password", widget=forms.PasswordInput, max_length=100)

    retyped_password = forms.CharField(
        label="retype password", widget=forms.PasswordInput, max_length=100)

    email = forms.EmailField()

    username.widget.attrs.update({'class': 'form-control input-group mb-2'})
    password.widget.attrs.update({'class': 'form-control input-group mb-2'})
    retyped_password.widget.attrs.update({'class': 'form-control input-group mb-2'})
    email.widget.attrs.update({'class': 'form-control input-group mb-2'})

    def clean(self):

        super().clean()

        password = self.cleaned_data.get("password")

        password2 = self.cleaned_data.get("retyped_password")

        username = self.cleaned_data.get("username")

        email = self.cleaned_data.get("email")

        if User.objects.all().filter(email=email).exists():

            raise ValidationError("The email is already registerd.")

        if User.objects.all().filter(username=username).exists():

            raise ValidationError("The username is already used by someone.")

        if password != password2:

            raise ValidationError(
                "The re typed password differ from first password.")

        validate_password(password)

        UnicodeUsernameValidator(username)


class UnRegisterForm(forms.Form):
    username = forms.CharField(label="your username")
    
    username.widget.attrs.update({'class': 'form-control input-group mb-2'})
    

class ImageForm(ModelForm):

    class Meta:
        model = NoteImage
        fields = ['image']


class AddImage(forms.ModelForm):
    
    class Meta:
        model = NoteImage
        fields = ('image',)
