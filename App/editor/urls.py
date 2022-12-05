"""Binding URLs to views"""

from django.urls import path

from . import views

urlpatterns = [
    path('',views.note_list, name='editor'),
    path('noteedit/<int:id>:', views.note_edit, name='note_edit'),
    path('noteadd/', views.note_add, name='note_add'),
    path('noteDelete/<int:id>', views.note_delete, name='note_delete'),
    path('accounts/login/', views.login_, name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('accounts/register/',views.register_account, name="register_account"),
    path('accounts/unregister/',views.unregister_account, name="unregister_account"),
]