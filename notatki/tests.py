from django.test import TestCase
from .models import Notatka
from django.urls import reverse
from django.contrib.auth.models import User

class IndexViewTests(TestCase):
    def setUp(self):
        """
        utworzenie i zalogowanie testowego użytkownika
        """
        User.objects.create_user(username='Adrian', password='12345')
        self.client.login(username='Adrian', password='12345')
    
    def test_no_notes(self):
        """
        0 notatek, czy strona działa
        """
        response = self.client.get(reverse('noteindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dodawanie notatki')

    def test_anonymous(self):
        """
        anonimowy powinien zostać przekierowany
        """
        self.client.logout()
        response = self.client.get(reverse('noteindex'))
        self.assertEqual(response.status_code, 302) #302 Redirection_FOUND

class NoteViewTests(TestCase):
    def setUp(self):
        """
        utworzenie i zalogowanie testowego użytkownika
        """
        User.objects.create_user(username='Adrian', password='12345')
        self.client.login(username='Adrian', password='12345')

    def test_new_note(self):
        """
        dodanie i wyświetlenie notatki
        """
        testtitle='notetesttitle'
        testcontent='lotoftext'
        response = self.client.post(reverse('add note'), {'title': testtitle, 'content': testcontent, 'publicnote': False})
        response = self.client.get(reverse('noteindex'))
        self.assertContains(response, testtitle)
        self.assertContains(response, testcontent)

    def test_save_changes(self):
        """
        dodanie i edytowanie notatki
        """
        testtitle='1title'
        testcontent='1content'
        edittitle='2title'
        editcontent='2content'
        #oryginalna notatka
        response = self.client.post(reverse('add note'), {'title': testtitle, 'content': testcontent, 'publicnote': False})
        response = self.client.get(reverse('noteindex'))
        self.assertContains(response, testtitle)
        self.assertContains(response, testcontent)
        #edycja notatki
        url=reverse('save changes', kwargs={"note_id": 1})
        editresponse = self.client.post(url, data={'title': edittitle, 'content': editcontent, 'publicnote': False})
        editresponse = self.client.get(reverse('noteindex'))
        self.assertContains(editresponse, edittitle)
        self.assertContains(editresponse, editcontent)

    def test_delete_note(self):
        """
        dodanie i usuwanie notatki
        """
        testtitle='notetodelete'
        testcontent='contenttodelete'
        #tworzenie
        response = self.client.post(reverse('add note'), {'title': testtitle, 'content': testcontent, 'publicnote': False})
        response = self.client.get(reverse('noteindex'))
        self.assertContains(response, testtitle)
        self.assertContains(response, testcontent)
        #usuwanie
        url=reverse('delete note', kwargs={"note_id": 1})
        deleteresponse = self.client.post(url)
        deleteresponse = self.client.get(reverse('noteindex'))
        self.assertNotContains(deleteresponse, testtitle)
        self.assertNotContains(deleteresponse, testcontent)

    def test_anonymous(self):
        """
        edycja i usuwanie przez niezalogowanego
        """
        testtitle='loggedtitle'
        testcontent='loggedcontent'
        edittitle='loggedouttitle'
        editcontent='loggedoutcontent'
        #oryginalna notatka
        response = self.client.post(reverse('add note'), {'title': testtitle, 'content': testcontent, 'publicnote': False})
        response = self.client.get(reverse('noteindex'))
        self.assertContains(response, testtitle)
        self.assertContains(response, testcontent)
        #wylogowanie
        self.client.logout()
        #edycja notatki
        editurl=reverse('save changes', kwargs={"note_id": 1})
        editresponse = self.client.post(editurl, data={'title': edittitle, 'content': editcontent, 'publicnote': False})
        self.assertEqual(editresponse.status_code, 403) #403 Forbidden
        #usuwanie notatki
        deleteurl=reverse('delete note', kwargs={"note_id": 1})
        deleteresponse = self.client.post(deleteurl)
        self.assertEqual(deleteresponse.status_code, 403) #403 Forbidden