from django.shortcuts import render, redirect
from .models import Receipt
from .forms import ReceiptForm

def home(request):

    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReceiptForm()

    receipts = Receipt.objects.all().order_by('-created_at')

    return render(request, 'home.html', {
        'receipts': receipts,
        'form': form
    })