from django.urls import path

from . import views

app_name = 'ankiety'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/wyniki/', views.ResultsView.as_view(), name='wyniki'),
    path('<int:question_id>/glos/', views.vote, name='vote'),
]