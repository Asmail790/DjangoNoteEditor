
from django.http import HttpResponse,request

from django.shortcuts import render

from .models import Note

from .forms import NoteForm, LoginForm,RegisterForm, UnRegisterForm

from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from django.contrib.auth import get_user

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@login_required()
def editor(request):

    
    user = User.objects.get(id=request.user.id)
    
    notes = Note.objects.all().filter(user=user)
    
    context = {'notes':notes}
    
    return render(request, 'editor/note/list/view.html', context)


@login_required()
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
    return render(request, 'editor/note/add_or_edit/view.html',context)

@login_required()
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
    return render(request, 'editor/note/add_or_edit/view.html',context)

@login_required()
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

    return render(request, 'editor/account/login/view.html', context)

@login_required()
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

    return render(request,'editor/account/register/view.html',context)

@login_required()
def unregister_account(request):
    
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
                
                messages.success(request,"username is incorrect")

                return redirect('unregister_account')
            
    context = {"form":unregisterform}
    return render(request,'editor/account/unregister/view.html',context)



