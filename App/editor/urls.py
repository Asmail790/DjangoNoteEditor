"""Binding URLs to views"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='editor'),

    path('noteedit/<int:id_>:', views.note_edit, name='note_edit'),
    path('noteadd/', views.note_add, name='note_add'),
    path('noteDelete/<int:id_>', views.note_delete, name='note_delete'),
    path('view/<int:id_>', views.note_view, name='note_view'),

    path('noteRemoveOrEditImage/<int:id_>',
         views.noteImage_remove_or_edit, name='remove_or_edit_image'),
    path('noteAddImage/<int:id_>', views.note_add_image, name='add_image'),

    path('accounts/login/', views.login_, name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('accounts/register/', views.register_account, name="register_account"),
    path('accounts/unregister/', views.unregister_account,
         name="unregister_account")
]
