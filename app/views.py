from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddExpenseForm
from .models import AddExpense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse

from collections import defaultdict

from budget.models import AddBudget
from income.models import AddIncome

import csv
import json

# Create your views here.

@login_required
def addExpense(request):
    form = AddExpenseForm()

    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

    all_entries = AddExpense.objects.filter(user=request.user).order_by('-id')
    edit_forms = {entry.id: AddExpenseForm(instance=entry) for entry in all_entries}

    notify_user = get_notification(request)

    return render(request, 'app/addExpense.html', {
        'form': form, 
        'all_entries': all_entries, 
        'edit_forms': edit_forms, 
        'notify_user': json.dumps(notify_user)})

@login_required
def deleteExpense(request, entry_id):
    entry = get_object_or_404(AddExpense, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
    return redirect('add_expense')  # from urls name

@login_required
def editExpense(request, entry_id):
    entry = get_object_or_404(AddExpense, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = AddExpenseForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
    else:
        form = AddExpenseForm(instance=entry)
    
    return redirect('add_expense')

@login_required
def get_notification(request):
    budgets = AddBudget.objects.filter(user=request.user)
    budget_map = defaultdict(float)

    for budget in budgets:
        key = budget.get_budget_category_display()
        budget_map[key] += float(budget.amount)

    expenses = AddExpense.objects.filter(user=request.user)
    expense_map = defaultdict(float)

    for expense in expenses:
        key = expense.get_exp_category_display()
        expense_map[key] += float(expense.amount)

    notification_info = []
    for category, budget_amnt in budget_map.items():
        expense_amnt = expense_map.get(category, 0)
        percentage = (expense_amnt/budget_amnt)* 100
        percentage = min(percentage, 100)
        notification_info.append({
            'category': category,
            'percentage': percentage
        })
    
    return notification_info

@login_required
def download_expense(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expense-for-{}.csv"'.format(request.user.username)

    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Custom-Category', 'Amount', 'Description'])

    expenses = AddExpense.objects.filter(user=request.user)
    for expense in expenses:
        date_str = expense.date.strftime('%Y-%m-%d')
        writer.writerow([date_str, expense.exp_category, expense.name, expense.amount, expense.comment])

    return response

