
from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.editor, name='editor'),
    path('noteedit/<int:id>:', views.noteEdit, name='note_edit'),
    path('noteadd/', views.noteAdd, name='note_add'),
    path('noteDelete/<int:id>', views.noteDelete, name='note_delete')
]
