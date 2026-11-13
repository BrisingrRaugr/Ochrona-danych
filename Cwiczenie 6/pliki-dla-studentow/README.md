# Laboratorium 6 — Cross-Site Scripting (poprawiona aplikacja)

Celowo podatna aplikacja „Tablica ogłoszeń” (Flask) z naprawionymi trzema
podatnościami XSS. Uruchamiać wyłącznie lokalnie.

## Uruchomienie

W katalogu z `compose.yaml`:

```text
docker compose up -d
```

- Aplikacja: http://127.0.0.1:8080
- Zbieracz (serwer napastnika, log żądań): http://localhost:8081
  — podgląd logu: `docker compose logs zbieracz`

Po każdej zmianie w `aplikacja/`:

```text
docker compose restart web
```

Zatrzymanie środowiska (zachowuje zmiany w `aplikacja/`):

```text
docker compose down
```

Konta ćwiczeniowe (dane fikcyjne): `anna` / `anna-lab6`, `student` / `student-lab6`.

## Wprowadzone poprawki

| Zadanie | Plik | Zmiana |
| 1 — XSS odbity | `aplikacja/app.py` (`/szukaj`) | `q` kodowane przez `html.escape()` przed wstawieniem do HTML |
| 2 — przejęcie sesji | `aplikacja/app.py` | `SESSION_COOKIE_HTTPONLY = True` (ciasteczko niedostępne dla `document.cookie`) |
| 3 — XSS zapisany | `aplikacja/templates/tablica.html` | usunięto filtr `|safe` — przywrócono auto-escaping Jinja2 |
| 3 — XSS DOM | `aplikacja/templates/podglad.html`, `aplikacja/static/podglad.js` | skrypt wyniesiony do pliku, `innerHTML` → `textContent` |
| 3 — CSP | `aplikacja/app.py` (`@app.after_request`) | nagłówek `Content-Security-Policy` na każdej odpowiedzi |

Szczegóły ataków i dowody: `dowody.md`.
