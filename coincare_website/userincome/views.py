import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import Source, UserIncome
from django.core.paginator import Paginator
from django.contrib import messages
from userpreferences.models import UserPreference

# Create your views here.

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        
        try:
            # Try to parse search_str as a month
            year_month = datetime.datetime.strptime(search_str, '%Y-%m')
            income = income.filter(date__year=year_month.year, date__month=year_month.month)
        except ValueError:
            pass

        data = income.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    filter_value = request.GET.get('filter', 'all')
    today = datetime.date.today()

    if filter_value == 'daily':
        start_date = today
    elif filter_value == 'weekly':
        start_date = today - datetime.timedelta(days=7)
    elif filter_value == 'monthly':
        start_date = today - datetime.timedelta(days=30)
    elif filter_value == '3months':
        start_date = today - datetime.timedelta(days=90)
    elif filter_value == '6months':
        start_date = today - datetime.timedelta(days=180)
    elif filter_value == 'yearly':
        start_date = today - datetime.timedelta(days=365)
    else:
        start_date = None  # No filter applied

    # Filter expenses based on the selected date range
    if start_date:
        income = UserIncome.objects.filter(owner=request.user, date__gte=start_date)
    else:
        income = UserIncome.objects.filter(owner=request.user)

    paginator = Paginator(income, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        user_preference = UserPreference.objects.get(user=request.user)
        currency = user_preference.currency
    except UserPreference.DoesNotExist:
        currency = 'USD'  # Set a default value or handle it as needed

    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
        'filter_value': filter_value
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/add_income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, date=date,
                               source=source, description=description)
        messages.success(request, 'Income saved successfully')

        return redirect('income')

@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources,
    }
    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit-income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit-income.html', context)

        income.amount = amount
        income. date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, 'Income updated  successfully')

        return redirect('income')
    
@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income removed')
    return redirect('income')

def income_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    
    # Fetch all income records within the last 6 months
    incomes = UserIncome.objects.filter(
        owner=request.user,
        date__gte=six_months_ago,
        date__lte=todays_date
    )
    
    # Initialize a dictionary to store the summarized data
    finalrep = {}

    # Helper function to extract the income source
    def get_source(income):
        return income.source

    # Get a unique list of sources
    source_list = list(set(map(get_source, incomes)))

    # Calculate the total amount for each source
    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount

    # Populate the summary dictionary with source and their total amounts
    for source in source_list:
        finalrep[source] = get_income_source_amount(source)
    
    # Return the summary data as JSON
    return JsonResponse({'income_category_data': finalrep}, safe=False)