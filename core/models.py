import os
import hashlib
import time
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .ocr import extract_text_from_receipt
from .parser import ReceiptParser
from .validators import validate_file_size, validate_file_extension


def get_hashed_file_path(instance, filename):

    ext = filename.split('.')[-1]

    unique_string = f"{filename}{time.time()}"

    filename_hash = hashlib.md5(unique_string.encode('utf-8')).hexdigest()

    return os.path.join('receipts_uploads/', f"{filename_hash}.{ext}")


class Receipt(models.Model):

    receipt_image = models.ImageField(
        upload_to=get_hashed_file_path,  # <--- TUTAJ PODPINAMY NOWĄ FUNKCJĘ
        validators=[
            validate_file_size,
            validate_file_extension
        ]
    )

    shop_name = models.CharField(max_length=100, blank=True, null=True)
    transaction_date = models.DateField(blank=True, null=True)
    transaction_total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paragon {self.id} ({self.shop_name or 'Nieznany'})"


@receiver(post_save, sender=Receipt)
def process_receipt_ai(sender, instance, created, **kwargs):
    if created:
        try:
            print(f"🤖 AI: Analiza paragonu #{instance.id}...")

            # 1. OCR (Czytanie)
            raw_text = extract_text_from_receipt(instance.receipt_image.path)

            # 2. Parser (Rozumienie)
            parser = ReceiptParser(raw_text)
            parsed_data = parser.parse()

            print(f"🧠 Zrozumiano: {parsed_data}")

            # 3. Zapisywanie do bazy
            needs_save = False

            if parsed_data['shop_name']:
                instance.shop_name = parsed_data['shop_name']
                needs_save = True

            if parsed_data['date']:
                instance.transaction_date = parsed_data['date']
                needs_save = True

            if parsed_data['total_amount']:
                instance.transaction_total_amount = parsed_data['total_amount']
                needs_save = True

            # Zapisujemy tylko wybrane pola, żeby nie wpaść w pętlę
            if needs_save:
                instance.save(update_fields=['shop_name', 'transaction_date', 'transaction_total_amount'])
                print("✅ Dane zaktualizowane w bazie!")

        except Exception as e:
            print(f"❌ Błąd AI: {e}")

