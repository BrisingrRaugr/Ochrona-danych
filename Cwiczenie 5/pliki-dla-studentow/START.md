# Środowisko laboratorium 5

Uruchom przed zajęciami. Wymagane: Docker z kontenerami Linux, Docker Compose, przeglądarka i curl. W Windows używaj `curl.exe` i Docker Desktop z WSL 2. Na Linuksie wystarczy Docker Engine z Compose. Wszystkie komendy wykonuj w katalogu zawierającym `compose.yaml`.

```text
docker version
docker compose version
docker compose build web
docker compose up -d web
docker compose exec web httpd -t
curl -i http://127.0.0.1:8080/
docker compose logs --tail 30 web
docker compose down
```

Oczekiwane: `Syntax OK`, HTTP 200 i strona „serwer WWW działa”. Przy pierwszej budowie potrzebny jest internet. Pakiet korzysta z obrazu `httpd:2.4-alpine` i instaluje Python 3. Po zbudowaniu zadania wykonuje się lokalnie. Zapis wersji środowiska: `docker compose exec web httpd -v` i `docker compose exec web python3 --version`.

## Co zmieniasz na zajęciach

- `konfiguracja/dostep.conf`: samodzielnie napisane reguły dostępu.
- `cgi-bin/uprawnienia.cgi`: własny program CGI, bez dostarczonego szkieletu.
- `auth/uzytkownicy`: lokalna baza tworzona narzędziem htpasswd; nie dodawaj jej do GitHuba.

Konfiguracja jest montowana do kontenera. Po jej zmianie sprawdź `httpd -t` i wykonaj `docker compose restart web`. CGI trafia do obrazu podczas budowy, dlatego po jego zmianie wykonaj `docker compose up -d --build web`. Dockerfile nadaje plikom `*.cgi` prawa wykonania. Zachowaj LF, także w pierwszej linii skryptu.

## Ścieżki

| Na komputerze | W kontenerze |
|---|---|
| `www/` | `/usr/local/apache2/htdocs/` |
| `cgi-bin/` | `/usr/local/apache2/cgi-bin/` |
| `auth/` | `/auth/` |
| `dane/` | `/lab-data/` |
| `konfiguracja/dostep.conf` | `/usr/local/apache2/conf/dostep.conf` |

`dane/` zawiera wyłącznie fikcyjne dane. Prawa odczytu są nadawane w obrazie, więc wynik eksperymentu nie zależy od uprawnień plików na Windows. W zadaniu sprawdzasz odczyt przez proces CGI, nie możliwość otwarcia źródłowej kopii na swoim komputerze.

## Rozwiązywanie problemów

- Zajęty port: w lokalnym pliku `.env` zapisz `LAB05_PORT=18080`. W adresach używaj wtedy portu 18080. Nie zmieniaj nasłuchiwania na wszystkie interfejsy hosta.
- Kontener nie startuje po zmianie reguł: `docker compose run --rm --no-deps web httpd -t` pokaże błąd także przy zatrzymanym serwerze.
- HTTP 500 z CGI: sprawdź `docker compose logs --tail 30 web`, interpreter, końce wierszy LF i pustą linię po Content-Type. Przebuduj obraz po zmianie kodu.
- Przeglądarka zapamiętuje logowanie: do porównania prób używaj osobnych wywołań curl.
- Ścieżka konfiguracji ma być plikiem. Uruchamiaj Compose w kompletnie rozpakowanym pakiecie.

Serwer udostępnia port wyłącznie na `127.0.0.1`. Nie używaj prawdziwych haseł. Polecenie `docker compose down` zatrzymuje środowisko tego pakietu i zachowuje lokalną konfigurację, kod oraz bazę ćwiczeniową.
