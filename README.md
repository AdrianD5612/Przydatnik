# Przydatnik

[![en](https://img.shields.io/badge/lang-pl-green.svg)](https://github.com/AdrianD5612/Przydatnik/blob/main/README.pl.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

An application in the form of a web page, running on the **Django (Python)** framework, allowing the recording of expenses, notes, and surveys that can be shared with other users, such as household members. Currently, it consists of the following modules:

1. Surveys
2. Expenses
3. Notes

**Surveys**: Allows you to ask questions with multiple answers.  
**Expenses**: Allows recording the history of expenses and income in a shared budget. The budget can also be set individually for each user.  
**Notes**: Allows you to store text notes, saved individually or publicly for everyone. They support Markdown formatting.

Additional settings:  
*SHARED_MODE*: Only works for the expenses module. It combines the expenses of all users into one common record instead of maintaining an individual list for each person.  
*ALLOW_REGISTRATION*: An option that allows public registration of new accounts. When turned off, only the administrator can create new accounts.

## Installation

1. Clone this repository.
2. Run `pip install -r requirements.txt`.
3. In the main directory, create a `.env` file.
4. In the `.env` file, write:  
   SECRET_KEY = 'your Django secret key'`  
   (You can generate the key, for example, on [this](https://djecrety.ir) website.)
5. Run `python manage.py makemigrations`.
6. Run `python manage.py migrate`.
7. You're done. To run the local test server:
8. Run `python manage.py runserver`.

___
The following tutorials were used:  
[Writing your first Django app](https://docs.djangoproject.com/en/4.1/intro/tutorial01)  
[Creating a Budget Web App with Django](https://kristian-roopnarine.medium.com/creating-a-budget-web-app-with-django-655369b6d43c)  
[Django Image Upload](https://www.javatpoint.com/django-image-upload)
