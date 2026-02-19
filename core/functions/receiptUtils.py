from django.db.models import Sum, QuerySet
from decimal import Decimal
from core.models import Receipt
from django.shortcuts import redirect, get_object_or_404


def aggregate_expenses(receipts: QuerySet[Receipt]) -> Decimal:

    total_expenses = receipts.aggregate(total=Sum("transaction_total_amount")).get(
        "total"
    )

    if total_expenses is None:
        return Decimal("0.00")

    return Decimal(total_expenses).quantize(Decimal("0.00"))


def delete_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)

    if request.method == "POST":
        receipt.delete()

    return redirect("home")
