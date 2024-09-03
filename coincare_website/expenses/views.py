"""
Views for the Expenses app.
"""
import datetime
import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse

from userpreferences.models import UserPreference
from .models import Category, Expense
# Create your views here.
from django.contrib.auth.models import User

def search_expenses(request):
    """
    Search expenses based on the search text.
    """
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        expenses = (
            Expense.objects.filter(amount__istartswith=search_str, owner=request.user)
            | Expense.objects.filter(date__istartswith=search_str, owner=request.user)
            | Expense.objects.filter(
                description__icontains=search_str, owner=request.user
            )
            | Expense.objects.filter(category__icontains=search_str, owner=request.user)
        )

        # Filter by month if the search string is in a date format
        try:
            # Try to parse search_str as a month
            year_month = datetime.datetime.strptime(search_str, "%Y-%m")
            expenses = expenses.filter(
                date__year=year_month.year, date__month=year_month.month
            )
        except ValueError:
            pass  # Not a valid date format, continue with other filters

        data = list(expenses.values())
        return JsonResponse(data, safe=False)


@login_required(login_url="/authentication/login")
def index(request):
    """
    Render the index page with expenses filtered by date range.
    """
    categories = Category.objects.all()
    filter_value = request.GET.get("filter", "all")

    today = datetime.date.today()
    if filter_value == "daily":
        start_date = today
    elif filter_value == "weekly":
        start_date = today - datetime.timedelta(days=7)
    elif filter_value == "monthly":
        start_date = today - datetime.timedelta(days=30)
    elif filter_value == "3months":
        start_date = today - datetime.timedelta(days=90)
    elif filter_value == "6months":
        start_date = today - datetime.timedelta(days=180)
    elif filter_value == "yearly":
        start_date = today - datetime.timedelta(days=365)
    else:
        start_date = None  # No filter applied

    # Filter expenses based on the selected date range
    if start_date:
        expenses = Expense.objects.filter(owner=request.user, date__gte=start_date)
    else:
        expenses = Expense.objects.filter(owner=request.user)

    paginator = Paginator(expenses, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    try:
        user_preference = UserPreference.objects.get(user=request.user)
        currency = user_preference.currency
    except UserPreference.DoesNotExist:
        currency = "USD"  # Set a default value or handle it as needed

    context = {
        "expenses": expenses,
        "page_obj": page_obj,
        "currency": currency,
        "filter_value": filter_value,  # Pass the filter value to the context
    }
    return render(request, "expenses/index.html", context)


@login_required(login_url="/authentication/login")
def add_expense(request):
    """
    Add a new expense record.
    """
    categories = Category.objects.all()
    context = {"categories": categories, "values": request.POST}
    if request.method == "GET":
        return render(request, "expenses/add_expense.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]

        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, "Amount must be a number (integer or float)")
            return render(request, "expenses/index.html", context)

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/add_expense.html", context)
        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]

        if not description:
            messages.error(request, "description is required")
            return render(request, "expenses/add_expense.html", context)

        Expense.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            category=category,
            description=description,
        )
        messages.success(request, "Expense saved successfully")

        return redirect("expenses")


@login_required(login_url="/authentication/login")
def expense_edit(request, id):
    """
    Edit an existing expense record.
    """
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {"expense": expense, "values": expense, "categories": categories}
    if request.method == "GET":
        return render(request, "expenses/edit-expense.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]

        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, "Amount must be a number (integer or float)")
            return render(request, "expenses/index.html", context)

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/edit-expense.html", context)
        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]

        if not description:
            messages.error(request, "description is required")
            return render(request, "expenses/edit-expense.html", context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, "Expense updated  successfully")

        return redirect("expenses")


@login_required(login_url="/authentication/login")
def delete_expense(request, id):
    """
    Delete an expense record.
    """
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed")
    return redirect("expenses")


def expense_category_summary(request):
    """
    Get a summary of expenses by category for the past six months.
    """
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30 * 6)
    expenses = Expense.objects.filter(
        owner=request.user, date__gte=six_months_ago, date__lte=todays_date
    )
    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({"expense_category_data": finalrep}, safe=False)
