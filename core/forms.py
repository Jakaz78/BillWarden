# core/forms.py
from django import forms
from .models import Receipt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ["receipt_image"]
        widgets = {
            "receipt_image": forms.FileInput(
                attrs={"accept": "image/*", "class": "form-control"}
            )
        }
        labels = {
            "receipt_image": "Wgraj zdjęcie paragonu",
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "jan@example.com"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Nazwa użytkownika",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "jan_kowalski"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


