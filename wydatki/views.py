from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse, FileResponse, HttpResponseForbidden, HttpResponseNotFound
from .models import ExpenseInfo, Theme  
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Q
from wydatki.forms import ExpenseDetails  
import math
from django.conf import settings

def index(request): #generowanie strony głównej wydatków
    if request.user.is_authenticated:
        try:
            if settings.SHARED_MODE: #tryb wspólnych wydatków
                expense_items = ExpenseInfo.objects.order_by('-date_added')
                budget_total = ExpenseInfo.objects.aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
                expense_total = ExpenseInfo.objects.aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
            else:   #tryb własnych wydatków
                expense_items = ExpenseInfo.objects.filter(user_expense=request.user).order_by('-date_added')
                budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
                expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
            mode='dark' #domyślny motyw=ciemny
            if Theme.objects.filter(user_theme=request.user).exists():  #jeśli użytkownik już wybierał motyw
                mode= Theme.objects.get(user_theme=request.user).mode
            fig,ax=plt.subplots()
            ax.bar(['Wydatki','Budżet'], [math.ceil(abs(expense_total['expenses'])),math.ceil(budget_total['budget'])],color=['red','green'])
            if  mode=='dark':
                ax.set_title('Suma wydatków i budżet', color="w")
                plt.rcParams.update({ #ciemny motyw dla wykresu
                    "lines.color": "white",
                    "patch.edgecolor": "white",
                    "text.color": "black",
                    "axes.facecolor": "white",
                    "axes.edgecolor": "lightgray",
                    "axes.labelcolor": "white",
                    "xtick.color": "white",
                    "ytick.color": "white",
                    "grid.color": "lightgray",
                    "figure.facecolor": "black",
                    "figure.edgecolor": "black",
                    "savefig.facecolor": "black",
                    "savefig.edgecolor": "black"})
            else:
                ax.set_title('Suma wydatków i budżet', color="black")
                plt.rcParams.update(plt.rcParamsDefault)
            plt.savefig('wydatki/static/wydatki/expense.jpg')
        except TypeError:
            pass    #błąd w przypadku braku wpisów, nie trzeba reagować
        if expense_total['expenses']: #przekazanie wpisów oraz sumy do statystyk
            context = {'expense_items':expense_items,'budget':round(budget_total['budget'],2),'expenses':round(abs(expense_total['expenses']),2), 'remaining':round((budget_total['budget']-abs(expense_total['expenses'])),2)}
        else:   #naprawia błąd w przypadku braku wpisów
            context = {'expense_items':expense_items,'budget':budget_total['budget'],'expenses':(expense_total['expenses']), 'remaining':0 }
        context['form']= ExpenseDetails()
        context['mode']=mode
        return render(request,'wydatki/index.html',context=context)
    else:
        return HttpResponseRedirect('login')

def add_item(request):  #dodawanie wydatku
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ExpenseDetails(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user_expense = request.user #zanim formularz zostanie zapisany w bazie musi zawierać nazwę użytkownika
                obj.save()
        return redirect('/app')
    else:
        return HttpResponseRedirect('login')

def logout_view(request):   #wylogowanie
    logout(request)
    return HttpResponseRedirect('/')

def custom_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('app')
    else:
        return HttpResponseRedirect('login')


def sign_up(request):   #rejestracja nowego użytkownika
    if settings.ALLOW_REGISTRATION: #czy włączona jest możliwość rejestracji
        errors=''
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user=form.save()
                login(request,user)
                return HttpResponseRedirect('app')
            else:
                for msg in form.error_messages:
                    errors+=form.error_messages[msg]
                return render(request, 'wydatki/error.html', {
                'error_message': errors ,
                })
        else:
            form = UserCreationForm
            return render(request,'wydatki/sign_up.html',{'form':form})
    else:
        return render(request,'wydatki/sign_closed.html')

def theme(request): #wybranie motywu
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
    return redirect('/app')

def get_media(request,file):
    if request.user.is_authenticated:
        try:
            media_to_get=ExpenseInfo.objects.get(image='images/'+file)
        except ExpenseInfo.DoesNotExist:    #obrazek nie istnieje
            return HttpResponseNotFound()
        if media_to_get.user_expense==request.user or settings.SHARED_MODE: #jeśli użytkownik jest właścicielem LUB jest tryb wspólnych wydatków
            img = open('media/images/'+file, 'rb')
            response = FileResponse(img)
        else:
            response = HttpResponseForbidden()
    else:
        response = HttpResponseForbidden()
    return response