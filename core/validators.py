# core/validators.py
import os
from django.core.exceptions import ValidationError


def validate_file_size(value):

    limit_mb = 10
    limit_bytes = limit_mb * 1024 * 1024

    if value.size > limit_bytes:
        raise ValidationError(f"Plik jest za duży! Maksymalny rozmiar to {limit_mb} MB.")


def validate_file_extension(value):

    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']

    if not ext.lower() in valid_extensions:
        raise ValidationError("Nieobsługiwany format pliku. Dozwolone: JPG, PNG, BMP, WEBP.")