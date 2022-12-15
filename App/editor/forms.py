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

    username = forms.CharField(label='username', max_length=100)

    password = forms.CharField(widget=forms.PasswordInput, max_length=100)


class RegisterForm(forms.Form):

    # TODO add validiation
    # - password resaniable
    # - password == retyped_password samme

    username = forms.CharField(label='username', max_length=100)

    password = forms.CharField(
        label="password", widget=forms.PasswordInput, max_length=100)

    retyped_password = forms.CharField(
        label="retype password", widget=forms.PasswordInput, max_length=100)

    email = forms.EmailField()

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


class ImageForm(ModelForm):
    class Meta:

        model = NoteImage

        fields = ['image']


# NoteFormSet = modelformset_factory(Note, fields=(
#    'text', 'title'), extra=1)

NoteImageFormSet = inlineformset_factory(
    Note, NoteImage, fields=('image',), extra=1)
