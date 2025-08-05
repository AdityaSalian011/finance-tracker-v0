from django.shortcuts import render, redirect, get_object_or_404
from .models import AddIncome
from .forms import AddIncomeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import csv

# Create your views here.
@login_required 
def addIncome(request):
    if AddIncome.objects.filter(user=request.user).exists():
        return redirect('show_income')

    form = AddIncomeForm()
    if request.method == 'POST':
        form = AddIncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
        
            return redirect('show_income')
    return render(request, 'income/addIncome.html', {'form': form})

@login_required
def showIncome(request):
    entries = AddIncome.objects.filter(user=request.user)
    edit_entry = {entry.id: AddIncomeForm(instance=entry) for entry in entries}

    return render(request, 'income/showIncome.html', {'entries': entries, 'edit_entry': edit_entry}) 

@login_required
def editIncome(request, entry_id):
    entry = get_object_or_404(AddIncome, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = AddIncomeForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
        else:
            form = AddIncomeForm(instance=entry)
    
    return redirect('show_income')

@login_required
def download_income(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="income-for-{}.csv"'.format(request.user.username)

    writer = csv.writer(response)
    writer.writerow(['Date', 'Monthly Income', 'Business Income', 'Freelance Income', 'Other Income'])

    incomes = AddIncome.objects.filter(user=request.user)
    for income in incomes:
        date_str = income.date.strftime('%Y-%m-%d')
        writer.writerow([date_str, income.monthly_income, income.business_income, income.freelance_income, income.other_income])

    return response
