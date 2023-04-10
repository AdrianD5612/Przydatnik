from django.test import TestCase
import datetime
from .models import ExpenseInfo
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class IndexViewTests(TestCase):
    def setUp(self):
        """
        utworzenie i zalogowanie testowego użytkownika
        """
        User.objects.create_user(username='Adrian', password='12345')
        self.client.login(username='Adrian', password='12345')
    
    def test_no_expenses(self):
        """
        0 wydatków, czy wieświetlone jest 0 zł
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Zostało : <span style="color:blue;">0</span> złotych</h3>')

    def test_anonymous(self):
        """
        anonimowy powinien zostać przekierowany
        """
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302) #302 Redirection_FOUND

class Add_ItemViewTests(TestCase):
    def setUp(self):
        """
        utworzenie i zalogowanie testowego użytkownika
        """
        User.objects.create_user(username='Adrian', password='12345')
        self.client.login(username='Adrian', password='12345')

    def test_new_expense(self):
        """
        dodanie i wyświetlenie wydatku
        """
        testname='test'
        testcost=999
        # utworzenie testowego wydatku
        response = self.client.post(reverse('add item'), {'expense_name': testname, 'cost': testcost, 'date_added': datetime.date.today()})
        response = self.client.get(reverse('index'))
        self.assertContains(response, testname)
        self.assertContains(response, testcost)

    def test_more_expenses(self):
        """
        3 wydatki i sprawdzenie sum
        """
        response = self.client.post(reverse('add item'), {'expense_name': 'test1', 'cost': 10, 'date_added': datetime.date.today()})
        response = self.client.post(reverse('add item'), {'expense_name': 'test2', 'cost': 20, 'date_added': datetime.date.today()})
        response = self.client.post(reverse('add item'), {'expense_name': 'test3', 'cost': -20, 'date_added': datetime.date.today()})
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Twój całkowity budżet to: <span style="color:green;">30')    #budżet
        self.assertContains(response, 'Wydałeś w sumie : <span style="color:red;">20')  #wydałeś
        self.assertContains(response, 'Zostało : <span style="color:blue;">10') #zostało

class Sign_UpViewTests(TestCase):
    def test_registration(self):
        """
        rejestracja nowego użytkownika
        """
        username='PanTestowy'
        badPassword='1234'
        password='agHh1478'
        self.client.login
        if settings.ALLOW_REGISTRATION:
            #hasło niezgodne z wymogami
            response = self.client.post(reverse('sign up'), {'username':  username, 'password1': badPassword, 'password2': badPassword})
            self.assertContains(response, 'Błąd:')
            #różne hasła
            response = self.client.post(reverse('sign up'), {'username':  username, 'password1': password, 'password2': badPassword})
            self.assertContains(response, 'Błąd:')
            #prawidłowe dane
            response = self.client.post(reverse('sign up'), {'username':  username, 'password1': password, 'password2': password})
            self.assertRedirects(response, '/app', status_code=302, target_status_code=200) 
        else:
            response = self.client.post(reverse('sign up'), {'username':  username, 'password': password, 'Confirm password': password})
            self.assertContains(response,'Rejestracja jest zamknięta. Skontaktuj się z administratorem w celu utworzenia nowego konta.')

class ThemeViewTests(TestCase):
    def setUp(self):
        """
        utworzenie i zalogowanie testowego użytkownika
        """
        User.objects.create_user(username='Adrian', password='12345')
        self.client.login(username='Adrian', password='12345')
    def test_theme(self):
        """
        zmiana motywu na jasny,ciemny
        """
        mode='white'
        response = self.client.get('/theme', data={'mode': mode})
        response = self.client.get('/app')
        self.assertContains(response, 'whitestyle.css')
        mode='dark'
        response = self.client.get('/theme', data={'mode': mode})
        response = self.client.get('/app')
        self.assertContains(response, 'darkstyle.css')