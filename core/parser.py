import re
from datetime import datetime
from decimal import Decimal


class ReceiptParser:
    def __init__(self, raw_text):
        self.text = raw_text
        self.clean_lines = self._filter_tax_lines(raw_text.split('\n'))
        self.clean_text_no_tax = "\n".join(self.clean_lines)

    def parse(self):
        """Główna funkcja zwracająca dane"""
        amount = self._find_total_amount_by_keyword()

        if not amount:
            amount = self._find_max_amount()

        return {
            'shop_name': self._find_shop_name(),
            'date': self._find_date(),
            'total_amount': amount
        }

    def _filter_tax_lines(self, lines):
        cleaned = []
        for line in lines:
            # Jeśli linia zawiera PTU lub VAT, pomijamy ją
            if re.search(r'(PTU|VAT|NETTO|BRUTTO)', line, re.IGNORECASE):
                continue
            cleaned.append(line)
        return cleaned

    def _find_shop_name(self):
        known_shops = [
            'BIEDRONKA', 'LIDL', 'AUCHAN', 'CARREFOUR', 'KAUFLAND',
            'ŻABKA', 'ZABKA', 'ROSSMANN', 'ORLEN', 'SHELL', 'BP', 'CIRCLE K', 'DINO', 'LEWIATAN', "ROSSMANN"
        ]
        upper_text = self.text.upper()  # Szukamy w pełnym tekście
        for shop in known_shops:
            if shop in upper_text:
                return shop.title()

        if self.clean_lines and len(self.clean_lines) > 0:
            for line in self.clean_lines:
                if len(line.strip()) > 3:
                    return line.strip()[:50]
        return "Nieznany sklep"

    def _find_date(self):
        date_pattern = r'(\d{4}[-./]\d{2}[-./]\d{2})|(\d{2}[-./]\d{2}[-./]\d{4})'
        match = re.search(date_pattern, self.text)
        if match:
            date_str = match.group(0).replace('.', '-').replace('/', '-')
            try:

                if len(date_str.split('-')[0]) == 4:
                    return datetime.strptime(date_str, '%Y-%m-%d').date()

                else:
                    return datetime.strptime(date_str, '%d-%m-%Y').date()
            except ValueError:
                pass
        return None

    def _find_total_amount_by_keyword(self):
        candidates = []
        for line in self.clean_lines:

            if re.search(r'(SUMA\s+PLN|RAZEM|DO ZAPŁATY|TOTAL)', line, re.IGNORECASE):

                amounts = self._extract_all_amounts(line)
                if amounts:
                    candidates.extend(amounts)

        if candidates:

            return max(candidates)
        return None

    def _find_max_amount(self):

        all_amounts = self._extract_all_amounts(self.clean_text_no_tax)
        if all_amounts:
            return max(all_amounts)
        return None

    def _extract_all_amounts(self, text):

        candidates = re.findall(r'(\d+(?:[\s]\d+)*[.,]\d{2})', text)

        valid_amounts = []
        for c in candidates:

            clean_c = c.replace(' ', '').replace(',', '.')
            try:
                val = float(clean_c)

                if 0.01 < val < 3000:
                    valid_amounts.append(Decimal(str(val)))
            except ValueError:
                pass

        return valid_amounts