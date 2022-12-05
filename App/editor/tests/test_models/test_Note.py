from django.test import TestCase
from django.contrib.auth.models import User
from ...models import Note
from django.test import Client
from ... import views 
from ...urls import urlpatterns
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

    def test_note_cascade(self):
        
        self.user_asmail.delete()

        nbr_asmails_notes = len(Note.objects.all().filter(user=self.user_asmail))
        self.assertEqual(nbr_asmails_notes, 0)
    
    def test_create_note(self):
        
        nbr_notes_before = len(Note.objects.all().filter(user=self.user_asmail))
        self.create_Note(self.user_asmail,"note 7", "")
        
        nbr_notes_after = len(Note.objects.all().filter(user=self.user_asmail))
        self.assertEqual(nbr_notes_after, nbr_notes_before+1)

