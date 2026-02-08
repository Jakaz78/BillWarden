# core/forms.py
from django import forms
from .models import Receipt


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['receipt_image']
        widgets = {
            'receipt_image': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-control'})
        }
        labels = {
            'receipt_image': 'Wgraj zdjęcie paragonu',
        }