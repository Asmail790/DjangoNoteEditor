"""Contain django view for the app."""

from django import forms
from django.forms import inlineformset_factory
from django.urls import reverse
from django.urls.resolvers import URLResolver
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.http import HttpResponse

from django.shortcuts import render

from django.contrib.auth.models import User

from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth import get_user

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

from .models import Note, NoteImage

from .forms import AddImage, NoteForm, LoginForm, RegisterForm, UnRegisterForm


@login_required()
def note_list(request):
    """
    A view where all notes owned by curent logged in user are listed.
    """

    user = User.objects.get(id=request.user.id)

    notes = Note.objects.all().filter(user=user)
    context = {'notes': notes}

    return render(request, 'editor/note/list/view.html', context)


@login_required()
def note_edit(request, id_: int):
    """
    A view where a note can be edited.

    parameters:
    id: the id of the note which will be edited.
    """

    user = get_user(request)

    try:
        note = Note.objects.get(id=id_, user=user)

    except ObjectDoesNotExist:

        return HttpResponse("note don't exist")

    noteform = NoteForm(instance=note)

    if request.method == "POST":
        noteform = NoteForm(request.POST, instance=note)
        noteform.save()

        return redirect('editor')

    images = Note.objects.get(id=id_).noteimage_set.all()

    context = {'form': noteform, 'images': images}
    return render(request, 'editor/note/add_or_edit/view.html', context)


@login_required()
def note_add(request):
    """
    A view where a new note is added to curent logged in user.
    """
    noteform = NoteForm()

    if request.method == "POST":

        user = get_user(request)

        noteform = NoteForm(request.POST)

        note = noteform.save(commit=False)

        note.user = user

        note.save()

        noteform.save_m2m()

        return redirect('editor')

    context = {'form': noteform}
    return render(request, 'editor/note/add_or_edit/view.html', context)


@login_required()
def note_view(request: HttpRequest, id_):

    note = Note.objects.get(id=id_)
    images = note.noteimage_set.all()

    context = {'note': note, 'images': images}

    return render(request, 'editor/note/view_note/view.html', context)


@login_required()
def noteImage_remove_or_edit(request: HttpRequest, id_):
    note = Note.objects.get(id=id_)
    EditImageSet = inlineformset_factory(
        Note, NoteImage, fields=('image',), extra=0)

    EditImageForm = EditImageSet(instance=note)

    if request.method == "POST":
        EditImageForm = EditImageSet(
            data=request.POST, files=request.FILES, instance=note)
        if EditImageForm.is_valid():

            EditImageForm.save()

        return redirect('note_view', id_=note.pk)

    context = {'form': EditImageForm}
    return render(request, 'editor/note/edit_or_delete_images/view.html', context)


def note_add_image(request: HttpRequest, id_):
    note = Note.objects.get(id=id_)
    noteImage = NoteImage(note=note)
    form = AddImage()

    if request.method == "POST":
        form = AddImage(
            data=request.POST, files=request.FILES, instance=noteImage)
        if form.is_valid():
            form.save()
        return redirect('note_view', id_=id_)

    context = {'form': form}
    return render(request, 'editor/note/add_image/view.html', context)


@login_required()
def note_delete(request, id_: int):
    """
    A view where a note is deleted.

    paramters:
    id: the id of the note which be deleted.
    """

    user = get_user(request)

    try:

        note = Note.objects.get(id=id_, user=user)

    except ObjectDoesNotExist:

        return HttpResponse("note don't exist")

    note.delete()

    return redirect('editor')


def login_(request):
    """
    A view where user log in.
    """

    if request.user.is_authenticated:
        return redirect("editor")

    loginform = LoginForm()

    if request.method == "POST":

        loginform = LoginForm(request.POST)

        if loginform.is_valid():

            user = authenticate(
                username=loginform.cleaned_data['username'],
                password=loginform.cleaned_data['password']
            )

            if user:

                login(request, user)

                return redirect('editor')

            else:
                messages.success(
                    request, 'Login falid check password and username')

                return redirect('login')

    context = {'form': loginform}

    return render(request, 'editor/account/login/view.html', context)


@login_required()
def logout_view(request):
    """
    A view where user  logout.
    """

    logout(request)

    return redirect('editor')


def register_account(request):
    """
    A view where a new account is created.
    """

    registerform = RegisterForm()

    if request.method == "POST":

        registerform = RegisterForm(request.POST)

        if registerform.is_valid():

            user = User.objects.create_user(
                username=registerform.cleaned_data['username'],
                password=registerform.cleaned_data['password'],
                email=registerform.cleaned_data['email']
            )

            login(request, user)

            return redirect("editor")

        else:

            redirect("register_account")

    context = {"form": registerform}

    return render(request, 'editor/account/register/view.html', context)


@login_required()
def unregister_account(request):
    """
    A view where a account is deleted.
    """

    unregisterform = UnRegisterForm()

    if request.method == "POST":

        unregisterform = UnRegisterForm(request.POST)

        if unregisterform.is_valid():
            user = get_user(request)

            if user.username == unregisterform.cleaned_data['username']:

                logout(request)

                user.delete()

                return redirect('editor')

            else:

                messages.success(request, "username is incorrect")

                return redirect('unregister_account')

    context = {"form": unregisterform}
    return render(request, 'editor/account/unregister/view.html', context)
