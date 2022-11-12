
from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.editor, name='editor'),
    path('noteedit/<int:id>:', views.noteEdit, name='note_edit'),
    path('noteadd/', views.noteAdd, name='note_add'),
    path('noteDelete/<int:id>', views.noteDelete, name='note_delete'),
    path('accounts/login/', views.login_, name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('register/',views.register_account, name="register_account"),
    path('unregister/',views.unregister_account, name="unregister_account"),
]
