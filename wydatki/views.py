from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import ExpenseInfo
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Q
# Create your views here.


def index(request):
    expense_items = ExpenseInfo.objects.filter(user_expense=request.user).order_by('-date_added')
    try:
        budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
        expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
        fig,ax=plt.subplots()
        ax.bar(['Wydatki','Budżet'], [abs(expense_total['expenses']),budget_total['budget']],color=['red','green'])
        ax.set_title('Suma wydatków i budżet')
        plt.savefig('wydatki/static/wydatki/expense.jpg')
    except TypeError:
        print('Brak danych.')
    if expense_total['expenses']:
        context = {'expense_items':expense_items,'budget':budget_total['budget'],'expenses':abs(expense_total['expenses']), 'remaining':(budget_total['budget']-abs(expense_total['expenses']))}
    else:   #naprawia błąd w przypadku braku wpisów
        context = {'expense_items':expense_items,'budget':budget_total['budget'],'expenses':(expense_total['expenses']), 'remaining':(budget_total['budget']-expense_total['expenses'])}
    return render(request,'wydatki/index.html',context=context)

def add_item(request):
    name = request.POST['expense_name']
    expense_cost = request.POST['cost']
    expense_date = request.POST['expense_date']
    ExpenseInfo.objects.create(expense_name=name,cost=expense_cost,date_added=expense_date,user_expense=request.user)
    budget_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(budget=Sum('cost',filter=Q(cost__gt=0)))
    expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(expenses=Sum('cost',filter=Q(cost__lt=0)))
    fig,ax=plt.subplots()
    if expense_total['expenses']:
        ax.bar(['Wydatki','Budżet'], [abs(expense_total['expenses']),budget_total['budget']],color=['red','green'])
    else:
        ax.bar(['Wydatki','Budżet'], [expense_total['expenses'],budget_total['budget']],color=['red','green'])
    ax.set_title('Suma wydatków i budżet')
    plt.savefig('wydatki/static/wydatki/expense.jpg')
    return HttpResponseRedirect('app')


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