# core/ocr.py
import os
from PIL import Image  # Do zmniejszania zdjęć
import cv2  # Do wczytywania przez Paddle
import numpy as np

# Konfiguracja środowiska
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "1"
os.environ["FLAGS_allocator_strategy"] = 'naive_best_fit'
os.environ["FLAGS_fraction_of_gpu_memory_to_use"] = "0"

from paddleocr import PaddleOCR

print("⏳ Inicjalizacja modelu OCR... (To się stanie tylko raz)")

ocr_engine = PaddleOCR(
    lang='pl',
    enable_mkldnn=False
)
print("✅ Model OCR gotowy do pracy!")


def extract_text_from_receipt(image_path):
    print(f"🔍 OCR: Analizuję plik: {image_path}")

    try:
        img = Image.open(image_path)

        if max(img.size) > 1280:
            print(f"📉 Zmniejszam zdjęcie z {img.size} do max 1280px...")
            img.thumbnail((1280, 1280), Image.Resampling.LANCZOS)

            img_np = np.array(img)

            pass
        else:
            img_np = image_path

        result = ocr_engine.ocr(img_np)


        full_text = []


        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
            data = result[0]
            if 'rec_texts' in data:
                return "\n".join(data['rec_texts'])


        if result and isinstance(result, list):
            for line in result:
                if isinstance(line, list):
                    for word_info in line:
                        if isinstance(word_info, list) and len(word_info) >= 2:
                            text_tuple = word_info[1]
                            if isinstance(text_tuple, tuple) or isinstance(text_tuple, list):
                                full_text.append(text_tuple[0])

            if full_text:
                return "\n".join(full_text)

        return ""

    except Exception as e:
        print(f"❌ Błąd wewnątrz PaddleOCR: {e}")
        return ""