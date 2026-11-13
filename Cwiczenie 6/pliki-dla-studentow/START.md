# Środowisko laboratorium 6

Instrukcja na początek zajęć. Prowadzący wcześniej przygotowuje obrazy i narzędzia na stanowiskach; poniższe kroki budowania i pobierania służą także temu przygotowaniu. Wymagane: Docker z kontenerami Linux, Docker Compose, przeglądarka z narzędziami deweloperskimi i curl. W Windows używaj `curl.exe` i Docker Desktop z WSL 2. Na Linuksie wystarczy Docker Engine z Compose. Wszystkie komendy wykonuj w katalogu zawierającym `compose.yaml`.

```text
docker version
docker compose version
docker compose build
docker compose up -d
curl -i http://127.0.0.1:8080/
curl -i http://localhost:8081/test
docker compose logs --tail 30
docker compose down
```

Oczekiwane: HTTP 200 i strona „Tablica ogłoszeń” na porcie 8080. Zbieracz odpowiada HTTP 204, a w logu pojawia się wiersz `ZEBRANO: /test`. Przy pierwszej budowie potrzebny jest internet. Pakiet korzysta z obrazu `python:3.12-alpine` i instaluje Flask 3.1.3. Zapis wersji: `docker compose exec web python --version`.

## Co zmieniasz na zajęciach

- `aplikacja/app.py`: kod aplikacji Flask.
- `aplikacja/templates/`: szablony HTML Jinja2.
- `aplikacja/static/`: pliki statyczne, w zadaniu 3 także własny `podglad.js`.

Katalog `aplikacja/` jest montowany do kontenera. Po każdej zmianie wykonaj `docker compose restart web`. Restart usuwa dodane ogłoszenia, bo aplikacja trzyma je w pamięci. Sesje pozostają ważne. Kod zbieracza w `zbieracz/` nie wymaga zmian.

## Adresy i konta

| Adres | Rola |
|---|---|
| `http://127.0.0.1:8080` | Aplikacja „Tablica ogłoszeń” |
| `http://localhost:8081` | Zbieracz napastnika, log: `docker compose logs zbieracz` |
| konto `anna`, hasło `anna-lab6` | Ofiara, ma prywatną notatkę |
| konto `student`, hasło `student-lab6` | Napastnik |

Aplikację otwieraj zawsze pod `127.0.0.1`, a zbieracz pod `localhost`. Ciasteczka nie są izolowane numerem portu. Różne nazwy hosta sprawiają, że przeglądarka nie wysyła ciasteczek aplikacji do zbieracza bez udziału skryptu. Wszystkie dane i hasła są fikcyjne.

## Rozwiązywanie problemów

- Zajęty port: w lokalnym pliku `.env` zapisz `LAB06_PORT=18080` lub `LAB06_ZBIERACZ_PORT=18081`. Zmień wtedy adresy w ładunkach. Nie zmieniaj nasłuchiwania na wszystkie interfejsy hosta.
- Brak zmian po edycji: wykonaj `docker compose restart web` i odśwież stronę z pominięciem pamięci podręcznej (Ctrl+F5).
- HTTP 500 po zmianie: `docker compose logs --tail 30 web` pokaże błąd Pythona.
- Zbieracz nic nie zapisuje: sprawdź w zakładce Network adres żądania oraz to, czy skrypt w ogóle się wykonał (Console).
- Dwa konta jednocześnie: użyj okna prywatnego albo innej przeglądarki.

Serwer udostępnia porty wyłącznie na `127.0.0.1`. Polecenie `docker compose down` zatrzymuje środowisko i zachowuje Twoje zmiany w `aplikacja/`.
