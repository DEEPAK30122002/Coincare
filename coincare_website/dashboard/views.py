"""
Views for the Dashboard application.
"""
from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum


from userincome.models import UserIncome
from expenses.models import Expense


def dashboard(request):
    """
    Display the dashboard with summaries of income and expenses for various periods.
    """

    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_three_months = today - timedelta(days=90)
    start_of_six_months = today - timedelta(days=183)

    # Fetch data
    total_income = (
        UserIncome.objects.filter(owner=request.user).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    total_expenses = (
        Expense.objects.filter(owner=request.user).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )

    income_data = {
        "today": UserIncome.objects.filter(owner=request.user, date=today).aggregate(
            Sum("amount")
        )["amount__sum"]
        or 0,
        "week": UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_week
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0,
        "month": UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_month
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0,
        "three_months": UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_three_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0,
        "six_months": UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_six_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0,
    }

    expenses_data = {
        "today": Expense.objects.filter(owner=request.user, date=today).aggregate(
            Sum("amount")
        )["amount__sum"]
        or 0,
        "week": Expense.objects.filter(
            owner=request.user, date__gte=start_of_week
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0,
        "month": Expense.objects.filter(
            owner=request.user, date__gte=start_of_month
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0,
        "three_months": Expense.objects.filter(
            owner=request.user, date__gte=start_of_three_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0,
        "six_months": Expense.objects.filter(
            owner=request.user, date__gte=start_of_six_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0,
    }

    # Weekly income and expenses by day
    weekly_income = {
        "monday": UserIncome.objects.filter(
            owner=request.user, date__week_day=2, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "tuesday": UserIncome.objects.filter(
            owner=request.user, date__week_day=3, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "wednesday": UserIncome.objects.filter(
            owner=request.user, date__week_day=4, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "thursday": UserIncome.objects.filter(
            owner=request.user, date__week_day=5, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "friday": UserIncome.objects.filter(
            owner=request.user, date__week_day=6, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "saturday": UserIncome.objects.filter(
            owner=request.user, date__week_day=7, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "sunday": UserIncome.objects.filter(
            owner=request.user, date__week_day=1, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
    }

    weekly_expenses = {
        "monday": Expense.objects.filter(
            owner=request.user, date__week_day=2, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "tuesday": Expense.objects.filter(
            owner=request.user, date__week_day=3, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "wednesday": Expense.objects.filter(
            owner=request.user, date__week_day=4, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "thursday": Expense.objects.filter(
            owner=request.user, date__week_day=5, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "friday": Expense.objects.filter(
            owner=request.user, date__week_day=6, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "saturday": Expense.objects.filter(
            owner=request.user, date__week_day=7, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
        "sunday": Expense.objects.filter(
            owner=request.user, date__week_day=1, date__range=[start_of_week, today]
        ).aggregate(total=Sum("amount"))["total"]
        or 0,
    }

    context = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": total_income - total_expenses,
        "income_data": income_data,
        "expenses_data": expenses_data,
        "weekly_income": weekly_income,
        "weekly_expenses": weekly_expenses,
    }

    return render(request, "dashboard/index.html", context)


def expense_summary(request):
    """
    Display a summary of expenses for various periods and categories.
    """
    today = timezone.now().date()  # Get today's date
    start_of_week = today - timedelta(
        days=today.weekday()
    )  # Get the start of the current week (Monday)
    start_of_month = today.replace(day=1)  # Get the start of the current month
    start_of_three_months = today - timedelta(days=90)
    start_of_six_months = today - timedelta(days=183)  # Approximation of 6 months

    # Filter the expenses based on the dates
    today_expenses = (
        Expense.objects.filter(owner=request.user, date=today).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    weekly_expenses = (
        Expense.objects.filter(owner=request.user, date__gte=start_of_week).aggregate(
            Sum("amount")
        )["amount__sum"]
        or 0
    )
    monthly_expenses = (
        Expense.objects.filter(owner=request.user, date__gte=start_of_month).aggregate(
            Sum("amount")
        )["amount__sum"]
        or 0
    )
    last_three_months_expenses = (
        Expense.objects.filter(
            owner=request.user, date__gte=start_of_three_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    last_six_months_expenses = (
        Expense.objects.filter(
            owner=request.user, date__gte=start_of_six_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    category_expenses = (
        Expense.objects.filter(owner=request.user)
        .values("category")
        .annotate(total_amount=Sum("amount"))
        .order_by("-total_amount")[:5]
    )

    context = {
        "today_expenses": today_expenses,
        "weekly_expenses": weekly_expenses,
        "monthly_expenses": monthly_expenses,
        "last_three_months_expenses": last_three_months_expenses,
        "last_six_months_expenses": last_six_months_expenses,
        "top_expenses": category_expenses,
    }
    return render(request, "dashboard/expense_summary.html", context)


def income_summary(request):
    """
    Display a summary of income for various periods and categories.
    """
    today = timezone.now().date()  # Get today's date
    start_of_week = today - timedelta(
        days=today.weekday()
    )  # Get the start of the current week (Monday)
    start_of_month = today.replace(day=1)  # Get the start of the current month
    start_of_three_months = today - timedelta(days=90)
    start_of_six_months = today - timedelta(days=183)  # Approximation of 6 months

    # Filter the income based on the dates
    today_income = (
        UserIncome.objects.filter(owner=request.user, date=today).aggregate(
            Sum("amount")
        )["amount__sum"]
        or 0
    )
    weekly_income = (
        UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_week
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    monthly_income = (
        UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_month
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    last_three_months_income = (
        UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_three_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    last_six_months_income = (
        UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_six_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    category_income = (
        UserIncome.objects.filter(owner=request.user)
        .values("source")
        .annotate(total_amount=Sum("amount"))
        .order_by("-total_amount")[:5]
    )

    context = {
        "today_income": today_income,
        "weekly_income": weekly_income,
        "monthly_income": monthly_income,
        "last_three_months_income": last_three_months_income,
        "last_six_months_income": last_six_months_income,
        "top_income": category_income,
    }
    return render(request, "dashboard/income_summary.html", context)


def balance_summary(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_last_three_months = today - timedelta(days=90)
    start_of_last_six_months = today - timedelta(days=180)

    # Calculate income and expenses for each period
    today_income = (
        UserIncome.objects.filter(owner=request.user, date=today).aggregate(
            Sum("amount")
        )["amount__sum"]
        or 0
    )
    today_expenses = (
        Expense.objects.filter(owner=request.user, date=today).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    weekly_income = (
        UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_week
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    weekly_expenses = (
        Expense.objects.filter(owner=request.user, date__gte=start_of_week).aggregate(
            Sum("amount")
        )["amount__sum"]
        or 0
    )
    monthly_income = (
        UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_month
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    monthly_expenses = (
        Expense.objects.filter(owner=request.user, date__gte=start_of_month).aggregate(
            Sum("amount")
        )["amount__sum"]
        or 0
    )
    last_three_months_income = (
        UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_last_three_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    last_three_months_expenses = (
        Expense.objects.filter(
            owner=request.user, date__gte=start_of_last_three_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    last_six_months_income = (
        UserIncome.objects.filter(
            owner=request.user, date__gte=start_of_last_six_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )
    last_six_months_expenses = (
        Expense.objects.filter(
            owner=request.user, date__gte=start_of_last_six_months
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )

    # Grand totals (this could also be the entire dataset, not just a sum of specific periods)
    total_income = (
        UserIncome.objects.filter(owner=request.user).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    total_expenses = (
        Expense.objects.filter(owner=request.user).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )

    # Context to pass to the template
    context = {
        "today_balance": today_income - today_expenses,
        "weekly_balance": weekly_income - weekly_expenses,
        "monthly_balance": monthly_income - monthly_expenses,
        "last_three_months_balance": last_three_months_income
        - last_three_months_expenses,
        "last_six_months_balance": last_six_months_income - last_six_months_expenses,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": total_income - total_expenses,
    }

    return render(request, "dashboard/balance_summary.html", context)
