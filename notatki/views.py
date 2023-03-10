from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import Notatka 
from wydatki.models import Theme
from django.db.models import Q

def index(request):
    try:
        note_list = Notatka.objects.filter(Q(author=request.user) | Q(publicnote=True)).order_by('-date_added') #Q umożliwia łączone wyrażenie typu OR
    except TypeError:
        print('Brak danych.')
    mode='dark' #domyślny motyw=ciemny
    if Theme.objects.filter(user_theme=request.user).exists():
        mode= Theme.objects.get(user_theme=request.user).mode
    context = {'note_list':note_list, 'mode':mode}
    return render(request,'index.html',context=context)

def theme(request):
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
    return redirect('/notatki')