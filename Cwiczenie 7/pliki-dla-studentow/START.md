# Środowisko laboratorium 7

Instrukcja na początek zajęć. Prowadzący wcześniej przygotowuje obrazy i narzędzia na stanowiskach; poniższe kroki budowania i pobierania służą także temu przygotowaniu. Wymagane: Docker z kontenerami Linux, Docker Compose, przeglądarka i curl. W Windows używaj `curl.exe` i Docker Desktop z WSL 2. Na Linuksie wystarczy Docker Engine z Compose. Wszystkie komendy wykonuj w katalogu zawierającym `compose.yaml`.

```text
docker version
docker compose version
docker compose build
docker compose up -d
curl -i "http://127.0.0.1:8080/sekret?klucz=1234"
curl -i "http://127.0.0.1:8080/kalkulator?wyrazenie=2*21"
docker compose logs --tail 30 web
docker compose down
```

Oczekiwane: HTTP 200, w sejfie „Liczba wierszy: 1” i sekret `Hello world`, w kalkulatorze wynik 42. Przy pierwszej budowie potrzebny jest internet. Pakiet korzysta z obrazu `python:3.12-alpine` i instaluje Flask 3.1.3. Baza `/dane/sekrety.db` powstaje podczas budowy obrazu i jest tylko do odczytu.

## Co zmieniasz na zajęciach

- `aplikacja/app.py`: kod aplikacji Flask, w tym zapytanie SQL i kalkulator.
- `aplikacja/templates/`: szablony HTML; zmiany nie są wymagane.

Katalog `aplikacja/` jest montowany do kontenera. Po każdej zmianie wykonaj `docker compose restart web`. Nie zmieniaj `Dockerfile`, `compose.yaml` ani `utworz_baze.py`. Kontener działa jako użytkownik `app` z systemem plików tylko do odczytu; to celowe ograniczenie skutków ataku.

## Rozwiązywanie problemów

- Zajęty port: w lokalnym pliku `.env` zapisz `LAB07_PORT=18080` i używaj tego portu w adresach. Nie zmieniaj nasłuchiwania na wszystkie interfejsy hosta.
- Znaki `'`, `#`, `+` i spacje w adresie: wpisuj wejście w formularz albo użyj `curl -G --data-urlencode "klucz=..." http://127.0.0.1:8080/sekret`. Znak `+` w adresie oznacza spację, a `#` rozpoczyna fragment.
- HTTP 500 po zmianie: `docker compose logs --tail 30 web` pokaże błąd Pythona.
- Brak zmian po edycji: wykonaj `docker compose restart web`.

Serwer udostępnia port wyłącznie na `127.0.0.1`. Polecenie `docker compose down` zatrzymuje środowisko i zachowuje Twoje zmiany w `aplikacja/`.
