from django.shortcuts import render
from app.models import AddExpense
from income.models import AddIncome
from budget.models import AddBudget

from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate

from collections import defaultdict
# Create your views here.

@login_required
def getDashboardInfo(request):
    total_income, total_expense = get_expense_income_total(request)
    balance = total_income - total_expense

    exp_custom_category_total = get_expense_category_data(request)
    exp_cat_labels = list(exp_custom_category_total.keys())
    exp_cat_values = list(exp_custom_category_total.values())

    # has_balance = total_income > 0 or total_expense > 0
    budget_tracker = get_budget_category_data(request)

    expense_dates, expense_amounts = get_expense_date_data(request)

    recent_transaction = get_recent_transaction_data(request)

    return render(request, 'dashboard/showDashboard.html', 
                  {'total_income': total_income, 
                   'total_expense': total_expense, 
                   'balance': balance, 
                   'exp_cat_labels': exp_cat_labels, 
                   'exp_cat_values': exp_cat_values, 
                   'budget_tracker': budget_tracker,
                   'expense_dates': expense_dates,
                   'expense_amounts': expense_amounts,
                   'recent_transaction': recent_transaction,
                   })

@login_required
def get_expense_income_total(request):
    income_totals = AddIncome.objects.filter(user=request.user).aggregate(
        monthly_total = Sum('monthly_income'),
        business_total = Sum('business_income'),
        freelance_total = Sum('freelance_income'),
        other_total = Sum('other_income'),
    )

    monthly_inc_total = income_totals['monthly_total'] or 0
    business_inc_total = income_totals['business_total'] or 0
    freelance_inc_total = income_totals['freelance_total'] or 0
    other_inc_total = income_totals['other_total'] or 0

    total_income = monthly_inc_total + business_inc_total + freelance_inc_total + other_inc_total

    total_expense = AddExpense.objects.filter(user=request.user).aggregate(
        total_amount = Sum('amount')
    )['total_amount'] or 0

    return total_income, total_expense

@login_required
def get_expense_category_data(request):
    expenses = AddExpense.objects.filter(user=request.user)
    category_totals = defaultdict(float)

    for expense in expenses:
        key = expense.name if expense.name else expense.get_exp_category_display()
        category_totals[key] += float(expense.amount)

    return category_totals

@login_required
def get_budget_category_data(request):
    budgets = AddBudget.objects.filter(user=request.user)
    budget_category_totals = defaultdict(float)

    for budget in budgets:
        key = budget.get_budget_category_display()
        budget_category_totals[key] += float(budget.amount)

    expenses = AddExpense.objects.filter(user=request.user)
    expense_category_totals = defaultdict(float)

    for expense in expenses:
        key = expense.get_exp_category_display()
        expense_category_totals[key] += float(expense.amount)


    colors = ['#10B981', '#3B82F6', '#A855F7', '#FBBF24']

    bud_tracker = []

    for idx, (category, budget_amount) in enumerate(budget_category_totals.items()):
        expense_amount = expense_category_totals.get(category, 0)
        percentage = (expense_amount/budget_amount)* 100 if budget_amount else 0
        bud_tracker.append({
            'category': category,
            'budget_amount': budget_amount,
            'expense_amount': expense_amount,
            'percentage': min(percentage, 100),
            'colors': colors[idx]
        })
    
    return bud_tracker

@login_required
def get_expense_date_data(request): 
    date = AddExpense.objects.filter(user=request.user).order_by('date')
    date_map = defaultdict(float)

    for entry in date:
        date_str = entry.date.strftime('%Y-%m-%d')
        date_map[date_str] += float(entry.amount)

    labels = list(date_map.keys())
    values = list(date_map.values())

    return labels, values

@login_required
def get_recent_transaction_data(request):
    rec_transaction = AddExpense.objects.filter(user=request.user).order_by('-date')

    return rec_transaction