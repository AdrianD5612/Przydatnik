# Przydatnik

Aplikacja w formie strony internetowej działającej na frameworku **Django(Python)** i świadczącej przydatne usługi ułatwiające wymianę poglądów czy zapamiętywanie wspólnych (lub mniej) informacji.
Aktualnie składa się z następujących modułów:

1. Ankiety
2. Wydatki
3. Notatki

**Ankiety**: umożliwiają zadać pytanie do żytkownika aby wybrał jedną z wielu opcji  
**Wydatki**: umożliwiają notowanie historii kosztów oraz wpływów do wspólnego budżetu. Budżet można też ustawić jako indywidualny  
**Notatki**: umożliwiają przechowywanie notatek tekstowych, zapisanych indywidualnie jak i publicznie dla wszystkich, które zostaną wyświetlone z formatowaniem Markdown  
  
Ustawienia dodatkowe:  
*SHARED_MODE*: działa tylko dla modułu wydatki. Tryb łączenia wydatków wszystkich użytkowników w jedną całość zamiast prowadzenia indywidualnego spisu dla każdego z osobna.  
*ALLOW_REGISTRATION*: opcja otwierająca możliwość publicznego rejestrowania nowego konta. Po jej wyłączeniu tylko administrator będzie mógł tworzyć nowe konta.

## Instalacja

1. Sklonuj to repozytorium  
2. pip install -r requirements.txt
3. W głownym katalogu stwórz plik .env
4. Napisz w .env  
    SECRET_KEY = 'twój sekretny klucz do Django'  
    (klucz możesz wygenerować np. na [tej](https://djecrety.ir) stronie)
5. python manage.py makemigrations
6. python manage.py migrate
7. Gotowe. Aby uruchomić lokalny serwer testowy to wykonaj jeszcze:
8. python manage.py runserver

___
Kod źródłowy bazowany na następujących samouczkach:  
[Writing your first Django app](https://docs.djangoproject.com/en/4.1/intro/tutorial01)  
[Creating a Budget Web App with Django](https://kristian-roopnarine.medium.com/creating-a-budget-web-app-with-django-655369b6d43c)  
[Django Image Upload](https://www.javatpoint.com/django-image-upload)
