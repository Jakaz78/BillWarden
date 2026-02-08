from django.contrib import admin
from .models import Receipt

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop_name', 'transaction_date', 'transaction_total_amount', 'created_at')
    list_display_links = ('id', 'shop_name')

