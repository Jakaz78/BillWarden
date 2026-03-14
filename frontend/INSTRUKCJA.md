# 🖥️ BillWarden Frontend — Instrukcja

## Struktura

```
frontend/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── src/
│   ├── main.tsx                    # Entry point
│   ├── App.tsx                     # Routing
│   ├── vite-env.d.ts               # Vite TypeScript types
│   ├── api/
│   │   └── client.ts              # Axios + JWT interceptor
│   ├── context/
│   │   ├── AuthContext.tsx         # Stan logowania
│   │   └── ThemeContext.tsx        # Dark/light mode
│   ├── components/
│   │   ├── Navbar.tsx             # Pasek nawigacji
│   │   ├── ProtectedRoute.tsx     # Ochrona tras
│   │   ├── ReceiptList.tsx        # Lista paragonów + podgląd
│   │   ├── ReceiptUpload.tsx      # Upload z drag & drop
│   │   ├── StatsCard.tsx          # Podsumowanie wydatków
│   │   └── MonthlyChart.tsx       # Wykres miesięczny (Recharts)
│   ├── pages/
│   │   ├── LoginPage.tsx          # Logowanie
│   │   ├── RegisterPage.tsx       # Rejestracja
│   │   └── DashboardPage.tsx      # Główny dashboard
│   ├── types/
│   │   └── index.ts               # Typy TypeScript
│   └── styles/
│       └── global.css             # Wszystkie style + dark mode
```

## Krok 1: Umieść folder

Skopiuj folder `frontend/` do katalogu głównego projektu (obok `core/`, `api/`, `BillWarden/`):

```
BillWarden/
├── api/
├── BillWarden/
├── core/
├── frontend/          ← TUTAJ
├── media/
├── static/
├── manage.py
└── requirements.txt
```

## Krok 2: Zainstaluj zależności

```bash
cd frontend
npm install
```

## Krok 3: Uruchom backend Django (w osobnym terminalu)

```bash
cd ..
python manage.py runserver
```

Backend musi działać na `http://127.0.0.1:8000`.

## Krok 4: Uruchom frontend

```bash
cd frontend
npm run dev
```

Frontend uruchomi się na `http://localhost:3000`.

## Jak to działa?

### Proxy (vite.config.ts)
Vite przekierowuje requesty `/api/*` i `/media/*` na Django (port 8000).
Dzięki temu nie ma problemów z CORS w trybie dev — React i Django wyglądają jak jeden serwer.

### JWT Flow
1. Login → POST `/api/auth/token/` → dostajemy `access` + `refresh`
2. Tokeny zapisane w `localStorage`
3. Każdy request dodaje `Authorization: Bearer <access>` (interceptor w Axios)
4. Gdy access wygaśnie (401) → automatyczny refresh
5. Gdy refresh wygaśnie → redirect na `/login`

### Routing
```
/login     → LoginPage (publiczny)
/register  → RegisterPage (publiczny)
/          → DashboardPage (chroniony — wymaga logowania)
```

### Dark Mode
Zapisuje się w `localStorage`. Respektuje systemowy motyw przy pierwszej wizycie.

## Krok 5: Build na produkcję

```bash
cd frontend
npm run build
```

Wygeneruje folder `dist/` z gotowymi plikami statycznymi.
Te pliki potem podepniemy pod Nginx w Docker Compose.

## Rozwiązywanie problemów

### "Network Error" / brak połączenia z API
Upewnij się, że Django działa na porcie 8000 i proxy w `vite.config.ts` jest poprawne.

### "401 Unauthorized" na każdym requeście
Token wygasł. Wyloguj się i zaloguj ponownie.

### Zdjęcia paragonów się nie ładują
Sprawdź czy Django serwuje pliki media (`MEDIA_URL` + `MEDIA_ROOT` w settings).
Proxy w Vite powinno przekierowywać `/media/*` na Django.
