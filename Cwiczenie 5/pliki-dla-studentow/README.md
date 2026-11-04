# Laboratorium 5 – Bezpieczeństwo serwera WWW

Lokalny Apache 2.4 w Dockerze z regułami dostępu i programem CGI.

- `konfiguracja/dostep.conf` – reguły dostępu (zadania 1–3)
- `cgi-bin/uprawnienia.cgi` – program CGI wypisujący UID/GID i wyniki odczytu `/lab-data`
- `raport.md`, `dowody.md` – wyniki

## Uruchomienie

Wymagany Docker z kontenerami Linux i Docker Compose.

docker compose build web
docker compose run --rm --no-deps narzedzia -cB /auth/uzytkownicy student
docker compose up -d web
docker compose exec web httpd -t


Baza haseł `auth/uzytkownicy` jest lokalna i nie trafia do repozytorium.

