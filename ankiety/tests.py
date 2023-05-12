import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def setUp(self):
        """
        utworzenie i zalogowanie testowego użytkownika
        """
        User.objects.create_user(username='Adrian', password='12345')
        self.client.login(username='Adrian', password='12345')
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() zwraca False dla ankiet z pub_date
        w przyszłości
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() zwraca False dla ankiet z pub_date
        starszym niż 1 dzień
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() zwraca True dla ankiet z pub_date
        w zakresie do 1 dnia
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    metoda na szybkie tworzenie ankiet testowych
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class IndexViewTests(TestCase):
    def setUp(self):
        """
        utworzenie i zalogowanie testowego użytkownika
        """
        User.objects.create_user(username='Adrian', password='12345')
        self.client.login(username='Adrian', password='12345')
    def test_no_questions(self):
        """
        czy jest wyświetlana wiadomość o braku ankiet
        """
        response = self.client.get(reverse('ankiety:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nie ma ankiet.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        czy pytania z przeszłości są wyświetlane na stronie głównej
        """
        question = create_question(question_text="Stare pytania.", days=-30)
        response = self.client.get(reverse('ankiety:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        czy pytania z przyszłości są wyświetlana
        """
        create_question(question_text="Przyszłe pytania.", days=30)
        response = self.client.get(reverse('ankiety:index'))
        self.assertContains(response, "Nie ma ankiet.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        czy jesli przyszłe i przeszłe istnieją to poprawnie jest wyświetlone
        """
        question = create_question(question_text="Stare pytania.", days=-30)
        create_question(question_text="Przyszłe pytania.", days=30)
        response = self.client.get(reverse('ankiety:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        czy dwie ankiety z przeszłości naraz są wyświetlane
        """
        question1 = create_question(question_text="Stare pytanie 1.", days=-30)
        question2 = create_question(question_text="Stare pytanie 2.", days=-5)
        response = self.client.get(reverse('ankiety:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

class DetailViewTests(TestCase):
    def setUp(self):
        """
        utworzenie i zalogowanie testowego użytkownika
        """
        User.objects.create_user(username='Adrian', password='12345')
        self.client.login(username='Adrian', password='12345')
    def test_future_question(self):
        """
        czy wyświetlanie ankiety z przyszłości zwraca błąd 404
        """
        future_question = create_question(question_text='Przyszłe pytanie.', days=5)
        url = reverse('ankiety:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        czy wyświetlanie ankiety z przeszłości pokazuje jej tekst
        """
        past_question = create_question(question_text='Stare pytanie.', days=-5)
        url = reverse('ankiety:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_not_existing_question(self):
        """
        czy wyświetlanie nieistniejącej ankiety zwraca błąd 404
        """
        url = reverse('ankiety:detail', args=(99,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)