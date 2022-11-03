from django.http import HttpResponse
from django.shortcuts import render
from .models import Note
from .forms import NoteForm
from .forms import NameForm
from django.shortcuts import redirect
# Create your views here.


def editor(request):
    notes = Note.objects.all()
    context = {'notes':notes}
    return render(request, 'editor/editor.html', context)

def noteEdit(request, id):
    note = Note.objects.get(id=id)
    noteform = NoteForm(instance = note)


    if request.method == "POST":
        noteform = NoteForm(request.POST, instance=note)
        noteform.save()

        return redirect('editor')


    context={'form':noteform}
    return render(request, 'editor/note.html',context)

def noteAdd(request):
    noteform = NoteForm()


    if request.method == "POST":
        noteform = NoteForm(request.POST)
        noteform.save()

        return redirect('editor')


    context={'form':noteform}
    return render(request, 'editor/note.html',context)

def noteDelete(request,id):
    print(id)
    note = Note.objects.get(id=id)
    note.delete()
    return redirect('editor')