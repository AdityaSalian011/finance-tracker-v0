from django.shortcuts import render, redirect, get_object_or_404
from .models import AddBudget
from .forms import AddBudgetForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import csv

# Create your views here.
@login_required
def addBudget(request):
    form = AddBudgetForm()
    if request.method == 'POST':
        form = AddBudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()

    all_entries = AddBudget.objects.filter(user=request.user).order_by('-id')
    edit_forms = {entry.id: AddBudgetForm(instance=entry) for entry in all_entries}

    return render(request, 'budget/addBudget.html', {'form':form, 'all_entries': all_entries, 'edit_forms': edit_forms})

@login_required
def add_custom_category(request):
    if request.method == 'POST':
        name = request.POST.get('name').title()
        if name:
            AddBudget.objects.get_or_create(name=name, user=request.user)
    
    return redirect('add_budget')

@login_required
def editBudget(request, entry_id):
    entry = get_object_or_404(AddBudget, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = AddBudgetForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
        else:
            form = AddBudgetForm(instance=entry)

    return redirect('add_budget')

@login_required
def deleteBudget(request, entry_id):
    entry = get_object_or_404(AddBudget, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
    
    return redirect('add_budget')

@login_required
def download_budget(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="budget-for-{}.csv"'.format(request.user.username)

    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Custom-Category', 'Amount', 'Description'])

    budgets = AddBudget.objects.filter(user=request.user)
    for budget in budgets:
        date_str = budget.date.strftime('%Y-%m-%d')
        writer.writerow([date_str, budget.budget_category, budget.name, budget.amount, budget.comment])

    return response