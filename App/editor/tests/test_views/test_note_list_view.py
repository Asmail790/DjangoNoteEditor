"""Multiple Test for for note list view."""


from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from ...models import Note
from ... import views



class TestNoteListView(TestCase):
    """Multiple Test for for note list view."""

    @classmethod
    def setUpTestData(cls):
        cls.user_asmail = User.objects.create_user(username="asmail", password="123456")
        cls.client =Client()
        cls.note_list_view_url = reverse(views.note_list)


    def test_context_contain_notes(self):
        """
        Test if response context contain the notes for curent loged in user.
        """
        self.client.login(username='asmail', password='123456')

        Note.objects.create(user = self.user_asmail,title="note 1", text="text")
        Note.objects.create(user = self.user_asmail,title="note 2", text="text")
        Note.objects.create(user = self.user_asmail,title="note 3", text="text")

        self.client.login(username='asmail', password='123456')

        notes_from_db = Note.objects.filter(user=User.objects.get(username="asmail"))

        response = self.client.get(self.note_list_view_url)

        notes_from_context = response.context["notes"]

        self.assertEqual(list(notes_from_db),list(notes_from_context))

    #       fix
    #       def test_redirct_to_login(self):
    #           response = self.client.get(self.note_list_view_url)
    #           login_url = reverse(views.login_)
    #           self.assertEqual(response.url, login_url)
