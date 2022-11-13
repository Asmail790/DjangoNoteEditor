from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Note
from django.test import Client
from .. import views 
from ..urls import urlpatterns
from django.urls import reverse

class TestDB(TestCase):
    
    @classmethod
    def create_Note(cls,user:User,title,text):
        Note.objects.create(user = user,title=title, text=text )
    
    @classmethod
    def setUpTestData(cls):
        cls.user_asmail = User.objects.create_user("asmail")
        cls.user_yousef = User.objects.create_user("yousef")

        cls.create_Note(cls.user_asmail, "note 1", "")
        cls.create_Note(cls.user_asmail, "note 2", "")
        cls.create_Note(cls.user_asmail, "note 3", "")

        cls.create_Note(cls.user_yousef, "note 4", "")
        cls.create_Note(cls.user_yousef, "note 5", "")
        cls.create_Note(cls.user_yousef, "note 6", "")

    def test_delete_user(self):
        
        self.user_asmail.delete()

        nbr_asmails_notes = len(Note.objects.all().filter(user=self.user_asmail))
        self.assertEqual(nbr_asmails_notes, 0)
    
    def test_create_note(self):
        
        nbr_notes_before = len(Note.objects.all().filter(user=self.user_asmail))
        self.create_Note(self.user_asmail,"note 7", "")
        
        nbr_notes_after = len(Note.objects.all().filter(user=self.user_asmail))
        self.assertEqual(nbr_notes_after, nbr_notes_before+1)


class TestNoteListView(TestCase):
    

    @classmethod
    def setUpTestData(cls):
        cls.user_asmail = User.objects.create_user(username="asmail", password="123456")
        cls.client =Client()
        cls.note_list_view_url = reverse(views.noteList)  


    def test_context_contain_notes(self):

        self.client.login(username='asmail', password='123456')

        Note.objects.create(user = self.user_asmail,title="note 1", text="text")
        Note.objects.create(user = self.user_asmail,title="note 2", text="text")
        Note.objects.create(user = self.user_asmail,title="note 3", text="text")
        
        self.client.login(username='asmail', password='123456')
        
        notes_from_db = Note.objects.filter(user=User.objects.get(username="asmail"))

        response = self.client.get(self.note_list_view_url)

        notes_from_context = response.context["notes"]

        self.assertEqual(list(notes_from_db),list(notes_from_context))

    def test_redirct_to_login(self):
        
        response = self.client.get(self.note_list_view_url)

        login_url = reverse(views.login_)

        self.assertEqual(response.url, login_url)






    



