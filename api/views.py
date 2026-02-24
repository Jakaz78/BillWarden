from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from decimal import Decimal

from core.models import Receipt
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ReceiptSerializer,
    ReceiptUploadSerializer,
    StatsSerializer,
)


# ====== Auth ======

class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ — rejestracja nowego użytkownika"""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    """GET /api/auth/me/ — dane zalogowanego użytkownika"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# ====== Receipts ======

class ReceiptListView(generics.ListAPIView):
    """GET /api/receipts/ — lista paragonów użytkownika (z paginacją)"""
    serializer_class = ReceiptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Receipt.objects
            .filter(user=self.request.user)
            .order_by("-transaction_date", "-created_at")
        )


class ReceiptUploadView(APIView):
    """POST /api/receipts/upload/ — wgrywanie paragonu"""
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReceiptUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receipt = serializer.save(user=request.user)
        return Response(
            ReceiptSerializer(receipt, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class ReceiptDeleteView(generics.DestroyAPIView):
    """DELETE /api/receipts/<id>/ — usuwanie paragonu"""
    serializer_class = ReceiptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user)


# ====== Stats ======

class StatsView(APIView):
    """GET /api/stats/ — statystyki wydatków użytkownika"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        receipts = Receipt.objects.filter(user=request.user)

        total = receipts.aggregate(
            total=Sum("transaction_total_amount")
        )["total"] or Decimal("0.00")

        count = receipts.count()

        monthly = (
            receipts
            .filter(transaction_date__isnull=False)
            .annotate(month=TruncMonth("transaction_date"))
            .values("month")
            .annotate(total=Sum("transaction_total_amount"))
            .order_by("-month")
        )

        data = {
            "total_expenses": Decimal(total).quantize(Decimal("0.01")),
            "receipt_count": count,
            "monthly_summary": list(monthly),
        }

        serializer = StatsSerializer(data)
        return Response(serializer.data)