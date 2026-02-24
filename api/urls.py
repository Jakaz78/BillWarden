from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # ====== Auth ======
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/me/", views.MeView.as_view(), name="me"),

    # ====== Receipts ======
    path("receipts/", views.ReceiptListView.as_view(), name="receipt_list"),
    path("receipts/upload/", views.ReceiptUploadView.as_view(), name="receipt_upload"),
    path("receipts/<int:pk>/", views.ReceiptDeleteView.as_view(), name="receipt_delete"),

    # ====== Stats ======
    path("stats/", views.StatsView.as_view(), name="stats"),
]