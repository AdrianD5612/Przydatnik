from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import Notatka 
from wydatki.models import Theme
from django.db.models import Q
from notatki.forms import NotatkaForm 
import datetime 

# TODO:guzik kolor napisu w dark mode niewidoczny

def index(request): #generowanie strony głównej notatek
    try:
        note_list = Notatka.objects.filter(Q(author=request.user) | Q(publicnote=True)).order_by('-date_added') #Q umożliwia łączone wyrażenie typu OR
    except TypeError:
        print('Brak danych.')
    mode='dark' #domyślny motyw=ciemny
    if Theme.objects.filter(user_theme=request.user).exists():  #jeśli użytkownik już wybierał motyw
        mode= Theme.objects.get(user_theme=request.user).mode
    context = {'note_list':note_list, 'mode':mode, 'form': NotatkaForm}
    return render(request,'index.html',context=context)

def add_note(request):  #dodawanie notatki
    if request.method == 'POST':
        form = NotatkaForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user #zanim notatka zostanie zapisana w bazie musi zawierać nazwę użytkownika
            obj.date_added = datetime.date.today()  #zanim notatka zostanie zapisana w bazie musi zawierać datę utworzenia
            obj.save()
        return redirect('/notatki')
    else:
        form = NotatkaForm()
        context = {
            'form': form
        }
    return render(request, 'index.html', context)

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
    return redirect('/notatki')