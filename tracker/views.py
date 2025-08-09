from django.shortcuts import render
from .models import currentbalance, Expense
from django.shortcuts import redirect, get_object_or_404
from decimal import Decimal
from django.db.models import Sum


# Create your views here.

def index(request):

    if request.method == 'POST':
        description = request.POST.get('description')
        amount = Decimal(request.POST.get('amount'))  # Convert to Decimal
        currency = request.POST.get('currency')
        tx_type = request.POST.get('type')
       
        current_balance = currentbalance.objects.first()
        
        if not current_balance:
            current_balance = currentbalance.objects.create(balance=0)
            
        # Update balance based on transaction type
        if tx_type == 'income':
            current_balance.balance += amount
        else:     
            current_balance.balance -= amount
           
        current_balance.save()

        Expense.objects.create(
            current_balance=current_balance,
            description=description,
            amount=amount,
            type=tx_type,
        )

        return redirect('index')

    expenses = Expense.objects.all().order_by('-date')
    current_balance = currentbalance.objects.first()

    income = Expense.objects.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    expense_total = Expense.objects.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'expenses': expenses,
        'current_balance': current_balance,
        'income': income,
        'expense': expense_total,
    }
    
    print(context)

    return render(request, 'index.html', context)


def delete_expense(request, expense_id):
    """Delete an expense and recalculate the current balance"""
    expense = get_object_or_404(Expense, id=expense_id)
    
    # Get the current balance object
    current_balance = expense.current_balance
    
    # Delete the expense
    expense.delete()
    
    # Recalculate balance from all remaining transactions
    total_income = Expense.objects.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Expense.objects.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    
    # Set the correct balance
    current_balance.balance = total_income - total_expense
    current_balance.save()
    
    return redirect('index')