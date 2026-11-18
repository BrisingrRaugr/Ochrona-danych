# Laboratorium 7 — SQL Injection i Code Injection (poprawiona aplikacja)

Celowo podatna aplikacja „Sejf sekretów" z kalkulatorem (Python, Flask, SQLite)
z naprawionymi trzema podatnościami. Uruchamiać wyłącznie lokalnie.

## Uruchomienie

W katalogu z `compose.yaml`:

```text
docker compose up -d
```

- Aplikacja: http://127.0.0.1:8080
- Sejf: `/sekret?klucz=1234`  ·  Kalkulator: `/kalkulator?wyrazenie=2*21`

Po każdej zmianie w `aplikacja/`:

```text
docker compose restart web
```

Logi serwera / zatrzymanie środowiska:

```text
docker compose logs --tail 30 web
docker compose down
```

Znaki `'`, `#`, `+`, spacje — wpisuj w formularz albo użyj
`curl.exe -G --data-urlencode "klucz=..." http://127.0.0.1:8080/sekret`.

## Wprowadzone poprawki

| Zadanie | Plik | Zmiana |
| 1/2 — SQL Injection | `aplikacja/app.py` (`sekret()`) | zapytanie z parametrem `?` i krotką `(klucz,)` zamiast sklejania napisu; treść SQL stała |
| 2 — ujawnianie błędów | `aplikacja/app.py` (`sekret()`) | ogólny komunikat dla użytkownika, szczegóły przez `app.logger.exception(...)` do logu |
| 3 — Code Injection | `aplikacja/app.py` (`kalkulator()`) | `eval` zastąpiony własnym parserem (liczba operator liczba), limit 100 znaków, HTTP 400 dla złego wejścia i dzielenia przez zero |
