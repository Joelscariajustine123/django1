import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User



def index(request):
    if request.method == 'POST':
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
    
    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))
    
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))
    
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))
    
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))
    
    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    
    categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    
    expense_form = ExpenseForm()
    
    return render(request,'trackerapp/index.html',
                  {'expense_form':expense_form,
                    'expenses':expenses,
                    'total_expenses':total_expenses,
                    'yearly_sum':yearly_sum,
                    'monthly_sum':monthly_sum,
                    'weekly_sum':weekly_sum,
                    'daily_sums':daily_sums,
                    'categorical_sums': categorical_sums
                    })


def edit(request,id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    
    if request.method == 'POST':
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid:
            form.save()
            return redirect('trackerapp/index')
  
    return render(request,'trackerapp/edit.html',{'expense_form':expense_form})


class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy("index")

# Login page for user
def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username).first()
            # print(user_obj)
            if not user_obj:
                messages.error(request, "Username not found")
                return redirect('login')
            user_auth = authenticate(username=username, password=password)
            if user_auth:
                login(request, user_auth)
                return redirect('index')
            messages.error(request, "Wrong Password")
            return redirect('login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('register')
    return render(request, "trackerapp/login.html")

# Register page for user
def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('register')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('register')
    return render(request, "trackerapp/register.html")

# Logout function
def custom_logout(request):
    logout(request)
    return redirect('login')
