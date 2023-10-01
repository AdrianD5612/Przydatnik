from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from wydatki.models import Theme
import sharedfunctions

def index(request):
    recents=Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    mode='dark' #domyślny motyw=ciemny
    if Theme.objects.filter(user_theme=request.user).exists():  #jeśli użytkownik już wybierał motyw
                mode= Theme.objects.get(user_theme=request.user).mode
    context={'latest_question_list':recents, 'mode':mode}
    return render(request,'ankiety/index.html',context=context)

def detail(request, pk):
    details=Choice.objects.filter(question_id=pk)
    quest=Question.objects.filter(id=pk)
    if not quest: #ankieta nie istnieje
         return HttpResponseNotFound()
    else:
        quest=quest[0]
        if quest.pub_date<=timezone.now():
            mode='dark' #domyślny motyw=ciemny
            if Theme.objects.filter(user_theme=request.user).exists():  #jeśli użytkownik już wybierał motyw
                        mode= Theme.objects.get(user_theme=request.user).mode
            context={'details':details, 'quest':quest, 'mode':mode}
            return render(request,'ankiety/detail.html',context=context)
        else:
            return HttpResponseNotFound()

def results(request, pk):
    details=Choice.objects.filter(question_id=pk)
    quest=Question.objects.filter(id=pk)
    if not quest: #ankieta nie istnieje
        return HttpResponseNotFound()
    else:
        quest=quest[0]
        if quest.pub_date<=timezone.now():
            mode='dark' #domyślny motyw=ciemny
            if Theme.objects.filter(user_theme=request.user).exists():  #jeśli użytkownik już wybierał motyw
                        mode= Theme.objects.get(user_theme=request.user).mode
            context={'details':details, 'quest':quest, 'mode':mode}
            return render(request,'ankiety/wyniki.html',context=context)
        else:
            return HttpResponseNotFound()

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Błąd, ponowne wyświetlanie wyboru
        return render(request, 'ankiety/detail.html', {
            'question': question,
            'error_message': "Nic nie wybrałeś.",
        })
    else:
        selected_choice.votes = True
        selected_choice.save()
        # Przekierowanie po wysłaniu POST
        return HttpResponseRedirect(reverse('ankiety:wyniki', args=(question.id,)))
    
def theme(request): ##wybranie motywu
    sharedfunctions.theme(request)
    return redirect('/ankiety')