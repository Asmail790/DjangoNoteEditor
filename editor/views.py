
from django.http import HttpResponse,request

from django.shortcuts import render

from .models import Note

from .forms import NoteForm, LoginForm,RegisterForm

from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from django.contrib.auth import get_user

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@login_required(login_url='/editor/login/')
def editor(request):

    
    user = User.objects.get(id=request.user.id)
    
    notes = Note.objects.all().filter(user=user)
    
    context = {'notes':notes}
    
    return render(request, 'editor/editor.html', context)


@login_required(login_url='/editor/login/')
def noteEdit(request, id):

    user = get_user(request)

    try:
        
        note = Note.objects.get(id=id, user=user)
    
    except ObjectDoesNotExist: 

        return HttpResponse("note don't exist")
    
    # check user
    
    noteform = NoteForm(instance = note)


    if request.method == "POST":
        noteform = NoteForm(request.POST, instance=note)
        noteform.save()

        return redirect('editor')


    context={'form':noteform}
    return render(request, 'editor/note.html',context)

@login_required(login_url='/editor/login/')
def noteAdd(request):
    noteform = NoteForm()


    if request.method == "POST":
        
        user  = get_user(request)
        
        noteform = NoteForm(request.POST)
        
        note = noteform.save(commit=False)
        
        note.user = user

        note.save()

        noteform.save_m2m()

        return redirect('editor')


    context={'form':noteform}
    return render(request, 'editor/note.html',context)

@login_required(login_url='/editor/login/')
def noteDelete(request,id):
    
    user = get_user(request)

    try:

        note = Note.objects.get(id=id, user=user)
    
    except ObjectDoesNotExist: 

        return HttpResponse("note don't exist")
    
    note.delete()
    
    return redirect('editor')


def login_(request):

    if request.user.is_authenticated:
        return redirect("editor")
    
    loginform = LoginForm()

    if request.method == "POST":
        
        loginform = LoginForm(request.POST)
        
        if loginform.is_valid():
            
            user = authenticate(
                username = loginform.cleaned_data['username'],
                password = loginform.cleaned_data['password']
            )
            
            if user:
                
                login(request, user)

                return redirect('editor')
            
            else:
                messages.success(request, 'Login falid check password and username')
                
                return redirect('login')  
    
    context = {'form':loginform}

    return render(request, 'editor/login.html', context)

@login_required(login_url='/editor/login/')
def logout_view(request):
    
    logout(request)
    
    return redirect('editor')


def register_account(request):
    

    
    registerform = RegisterForm()
    if request.method == "POST":

        registerform = RegisterForm(request.POST)

        if registerform.is_valid():
           
            user = User.objects.create_user(
                username=registerform.cleaned_data['username'],
                password=registerform.cleaned_data['password'],
                email=registerform.cleaned_data['email']
                )
            
            login(request,user)
            
            return  redirect("editor")
        
        else:

            redirect("register_account")
    
    context = {"form":registerform}

    return render(request,'editor/register_account.html',context)

@login_required(login_url='/editor/login/') 