from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from wydatki.models import Theme

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
    quest=quest[0]
    mode='dark' #domyślny motyw=ciemny
    if Theme.objects.filter(user_theme=request.user).exists():  #jeśli użytkownik już wybierał motyw
                mode= Theme.objects.get(user_theme=request.user).mode
    context={'details':details, 'quest':quest, 'mode':mode}
    return render(request,'ankiety/detail.html',context=context)

def results(request, pk):
    details=Choice.objects.filter(question_id=pk)
    quest=Question.objects.filter(id=pk)
    quest=quest[0]
    mode='dark' #domyślny motyw=ciemny
    if Theme.objects.filter(user_theme=request.user).exists():  #jeśli użytkownik już wybierał motyw
                mode= Theme.objects.get(user_theme=request.user).mode
    context={'details':details, 'quest':quest, 'mode':mode}
    return render(request,'ankiety/wyniki.html',context=context)

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
    mode=request.GET.get('mode')

    if mode=='dark':
        if Theme.objects.filter(user_theme=request.user).exists():
            user_saving= Theme.objects.get(user_theme=request.user)
            user_saving.user_theme=request.user
            user_saving.mode='dark'
            user_saving.save()
        else:
            user2=Theme(user_theme=request.user, mode='dark')
            user2.save()
    elif mode=='white':
        if Theme.objects.filter(user_theme=request.user).exists():
            user_saving= Theme.objects.get(user_theme=request.user)
            user_saving.user_theme=request.user
            user_saving.mode='white'
            user_saving.save()
        else:
            user2=Theme(user_theme=request.user, mode='white')
            user2.save()
    return redirect('/ankiety')