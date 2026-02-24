from .forms import ReceiptForm
from django.shortcuts import render, redirect
from .models import Receipt
from django.db.models import Sum
from .functions.receiptUtils import aggregate_expenses
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required


@login_required
def home(request):

    if request.method == "POST":
        form = ReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.user = request.user
            receipt.save()
            return redirect("home")
    else:
        form = ReceiptForm()

    receipts = (
        Receipt.objects
        .filter(user=request.user)
        .order_by("-transaction_date")
    )
    total_expenses = aggregate_expenses(receipts)

    monthly_summary = (
        Receipt.objects
        .filter(user=request.user)
        .annotate(month=TruncMonth("transaction_date"))
        .values("month")
        .annotate(total=Sum("transaction_total_amount"))
        .order_by("-month")
    )

    return render(
        request,
        "home.html",
        {
            "receipts": receipts,
            "total_expenses": total_expenses,
            "form": form,
            "monthly_summary": monthly_summary,
        },
    )