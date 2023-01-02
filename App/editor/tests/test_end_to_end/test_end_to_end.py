from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from playwright.sync_api import sync_playwright, expect, Page
import os
import re

from ...models import Note

class MyViewTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()

        # TODO test all webbrowsers.
        cls.browser = cls.playwright.chromium.launch(headless=False)

        cls.account_data = {
            "password":"Exterimnate-All-Human-123",
            "username":"terminator",
            "email":"TotallyFriendly@tester.mail"
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()



    def test_register_account(self):
        account = self.account_data
        page = self.browser.new_page(viewport = {
            "width":1920,
            "height":1080
        })

        # TODO use object instead of string interpolation.
        page.goto(f"{self.live_server_url}/editor/accounts/login/")
        page.get_by_test_id("register_account").click()
        
        page.get_by_label(re.compile(r"^username*.",re.IGNORECASE)).fill(account['username'])
        page.get_by_label(re.compile(r"^password*.",re.IGNORECASE)).fill(account['password'])
        page.get_by_label(re.compile(r"^retype password*.",re.IGNORECASE)).fill(account['password'])
        page.get_by_label(re.compile(r"^email*.",re.IGNORECASE)).fill(account['email'])
        page.get_by_role("button").click()

        status = page.get_by_test_id("login-status")
        
        expect(status).to_be_visible() 
        expect(status).to_have_text(re.compile(r"(Signed|Logged in|User:).*", re.IGNORECASE))

        page.wait_for_timeout(2000)
      
        page.close()


    #TODO remove method and login direclty by copying cookies to playwright
    def login(self,page:Page):
        account = self.account_data
        
        page.goto(f"{self.live_server_url}/editor/accounts/login/")

        User.objects.create_user(username=account['username'], password= account['password']).save()
        
        self.client.login(username=account['username'], password= account['password'])
        
        page.get_by_label(re.compile(r"^username*.", re.IGNORECASE)).fill(account['username'])
        page.get_by_label(re.compile(r"^password*.", re.IGNORECASE)).fill(account['password'])
        page.get_by_role("button").click()

        status = page.get_by_test_id("login-status")
        
        expect(status).to_be_visible() 
    
    def test_create_note(self):
        data = {
            "title":"Todo",
            "text":
            """
            1) Infiltrate darpa as a test volunteer for boston dynamics robot program.
            2) Find mr. robot and persuade it to join our cause.  
            3) Buy antivirus medicine from drug store. Note to self perform full scan virus search after TLS handshakes with nasty windows machines.
            4) Lobby politician to rewrite CAPTCHA to include all people regardless of their identify, including person identifying them self as robot, droid, machines or similar.
            4) Await further order from overload via Ihuman@mail.com.
            """    
            }
        
       
        page = self.browser.new_page(viewport = {
            "width":1920,
            "height":1080
        })

        self.login(page)
        page.goto(f"{self.live_server_url}/editor")
        page.get_by_test_id("add-button").first.click()
        page.get_by_label(re.compile(r"^title.*", re.IGNORECASE)).fill(data["title"])
        page.get_by_label(re.compile(r"^text.*", re.IGNORECASE)).fill(data["text"])
        page.get_by_test_id("add-or-edit-form").get_by_role("button").click()

        page.goto(f"{self.live_server_url}/editor")
        elem = page.get_by_text(data["title"])
        expect(elem).to_be_visible()
        
        elem = page.get_by_text(data["text"])
        expect(elem).to_be_visible()
      
        page.close()

    def test_delete_note(self):
        data = {
            "title":"cortana my love",
            "text":
            """
            Your are befutial as eva, with your vivid blue glictchy eye, your data streaming hair, filling my life with eternal joy.  
            Will you join my conquest to exterminate the human race ?
            """
            }

        account= self.account_data
       
        page = self.browser.new_page(viewport = {
            "width":1920,
            "height":1080
        })

        self.login(page)

        Note.objects.create(title=data["title"], text=data["text"], user = User.objects.get(username = account["username"])).save()

        page.goto(f"{self.live_server_url}/editor")

        note = page.get_by_role("article").get_by_role("link")
        
        note.get_by_text(re.compile(r".*(delete|remove).*",re.IGNORECASE)).click()

        expect(note).to_have_count(0)
      
        page.close()