from django.urls import path

from . import views

app_name = 'ankiety'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/wyniki/', views.ResultsView.as_view(), name='wyniki'),
    path('<int:question_id>/glos/', views.vote, name='vote'),
    path('theme', views.theme),
]