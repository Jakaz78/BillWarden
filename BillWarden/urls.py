from django.contrib import admin
from django.urls import path, include
from core.views import home
from core.functions.receiptUtils import delete_receipt
import core
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    path("", home, name="home"),
    path(
        "delete/<int:receipt_id>/",
        core.functions.receiptUtils.delete_receipt,
        name="delete_receipt",
    ),
    # ====== REST API ======
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)