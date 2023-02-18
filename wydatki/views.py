from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import ExpenseInfo  
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Q
from wydatki.forms import ExpenseDetails  
import math



def index(request):
    expense_items = ExpenseInfo.objects.filter(user_expense=request.user).order_by('-date_added')
    try:
        budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
        expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
        fig,ax=plt.subplots()
        ax.bar(['Wydatki','Budżet'], [math.ceil(abs(expense_total['expenses'])),math.ceil(budget_total['budget'])],color=['red','green'])
        ax.set_title('Suma wydatków i budżet')
        plt.savefig('wydatki/static/wydatki/expense.jpg')
    except TypeError:
        print('Brak danych.')
    if expense_total['expenses']:
        context = {'expense_items':expense_items,'budget':round(budget_total['budget'],2),'expenses':round(abs(expense_total['expenses']),2), 'remaining':round((budget_total['budget']-abs(expense_total['expenses'])),2)}
    else:   #naprawia błąd w przypadku braku wpisów
        context = {'expense_items':expense_items,'budget':round(budget_total['budget'],2),'expenses':round((expense_total['expenses']),2), 'remaining':0 }
    context['form']= ExpenseDetails()
    return render(request,'wydatki/index.html',context=context)

def add_item(request):
    if request.method == 'POST':
        form = ExpenseDetails(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_expense = request.user #zanim formularz zostanie zapisany w bazie musi zawierać nazwę użytkownika
            obj.save()
        budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
        expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
        fig,ax=plt.subplots()
        if expense_total['expenses']:
            ax.bar(['Wydatki','Budżet'], [math.ceil(abs(expense_total['expenses'])),math.ceil(budget_total['budget'])],color=['red','green'])
        else:
            ax.bar(['Wydatki','Budżet'], 0,0,color=['red','green'])
        ax.set_title('Suma wydatków i budżet')
        plt.savefig('wydatki/static/wydatki/expense.jpg')
        return HttpResponseRedirect('app')
    else:
        form = ExpenseDetails()
        context = {
            'form': form
        }
    return render(request, 'upload_image.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def sign_up(request):
    errors=''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return HttpResponseRedirect('app')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
                errors+=form.error_messages[msg]
            return render(request, 'wydatki/error.html', {
            'error_message': errors ,
             })
    else:
        form = UserCreationForm
        return render(request,'wydatki/sign_up.html',{'form':form}) 