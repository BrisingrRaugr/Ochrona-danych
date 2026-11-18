# Laboratorium 7 - SQL Injection i Code Injection

**3 zadania po 1 pkt. 90 minut (2 × 45).** Plan: 10 minut wprowadzenia, 20 + 20 + 25 minut na zadania, 15 minut na raport i oddanie. Na początku zajęć uruchom przygotowane stanowisko według `START.md`. Atakujesz i naprawiasz dostarczoną, celowo podatną aplikację „Sejf sekretów” z kalkulatorem (Python, Flask, SQLite). Wejścia atakujące i poprawki piszesz samodzielnie.

Dozwolone: ISOD, dokumentacja, własne notatki i własny wcześniej napisany kod. Podczas zajęć wyłącz czaty i podpowiedzi LLM. Przy odbiorze wyjaśniasz ataki i poprawki. Atakujesz wyłącznie lokalną aplikację z pakietu, pod adresem `http://127.0.0.1:8080`.

## Uruchomienie i sprawdzanie

Wszystkie polecenia wykonuj w katalogu `pliki-dla-studentow`. Uruchom `docker compose up -d`. Kod aplikacji jest w `aplikacja/`; po każdej zmianie wykonaj `docker compose restart web`. Logi: `docker compose logs --tail 30 web`. Kontener ma system plików tylko do odczytu i działa jako użytkownik bez uprawnień administratora. Baza zawiera wyłącznie fikcyjne dane.

Wejścia wpisuj w formularze aplikacji albo w adres. Strona sejfu ma sekcję „Tryb diagnostyczny”, która pokazuje wykonane zapytanie, komunikat błędu i liczbę wierszy. W Windows używaj `curl.exe`; w curl kodowanie znaków zapewnia np. `curl -G --data-urlencode "klucz=..." http://127.0.0.1:8080/sekret`.

## Pomoc i zapis wyników

Pomoc podczas zajęć: `pliki-dla-studentow/PRZEWODNIK.md`. Raport ma jedną stronę: zwięzłe wyniki i wnioski. Długie polecenia, ładunki i logi możesz zapisać w `dowody.md` w repozytorium, wskazując sekcje w raporcie. Skracaj tokeny; nie zapisuj haseł ani kluczy prywatnych. Część dodatkowa nie jest wymagana na pełne 3 pkt.

## Zadanie 1 - SQL Injection (20 min, 1 pkt)

1. Otwórz `/sekret?klucz=1234`. W `aplikacja/app.py` znajdź miejsce, w którym klucz trafia do zapytania SQL.
2. Wpisz jako klucz sam apostrof `'`. Zapisz komunikat błędu i wyjaśnij, skąd się wziął.
3. Przygotuj wejście, które bez znajomości żadnego klucza zwraca wszystkie sekrety. Zapisz liczbę wierszy.
4. Użyj `UNION SELECT` i tabeli `sqlite_master`, aby poznać nazwy tabel bazy. Następnie odczytaj zawartość drugiej tabeli. Zapytanie aplikacji zwraca dwie kolumny.

**W raporcie:** pięć wejść z liczbą zwróconych wierszy, zapytanie po wstawieniu danych dla jednego ataku, nazwy tabel i kolumn drugiej tabeli oraz jedno zdanie: jak dane wejściowe zmieniły strukturę zapytania.

## Zadanie 2 - Zapytanie z parametrami (20 min, 1 pkt)

1. Zastąp sklejanie napisu zapytaniem z parametrem `?` i krotką wartości przekazaną do `execute`. Treść zapytania ma być stała.
2. Zamiast szczegółów wyjątku SQLite pokaż użytkownikowi ogólny komunikat. Szczegóły zapisz w logu serwera, np. `app.logger.exception(...)`.
3. Po restarcie powtórz pięć wejść z zadania 1 oraz klucz `d'Artagnan`, który istnieje w bazie i zawiera apostrof.
4. Sprawdź w logu i na stronie, czy jakikolwiek atak zwraca dane albo komunikat SQLite.

**W raporcie:** tabela sześciu wejść z liczbą wierszy przed poprawką i po niej, fragment kodu z parametrem oraz jedno zdanie: dlaczego wartość parametru nie może zmienić struktury zapytania. Dodaj, czy parametr może zastąpić nazwę tabeli.

## Zadanie 3 - Code Injection w kalkulatorze (25 min, 1 pkt)

1. Otwórz `/kalkulator?wyrazenie=2*21`. W `app.py` znajdź funkcję, która oblicza wyrażenie.
2. Bez zmieniania kodu, wyłącznie przez pole wyrażenia: wypisz zawartość katalogu `/etc` w kontenerze, odczytaj nazwę i wersję systemu z `/etc/os-release` oraz numer UID procesu aplikacji. Zapisz użyte wyrażenia.
3. Zastąp obliczanie własnym parserem. Dozwolony format: liczba, operator, liczba. Liczba może być ujemna i mieć część dziesiętną, wokół operatora mogą być spacje. Operatory z listy dozwolonych: `+`, `-`, `*`, `/`. Ogranicz długość wejścia do 100 znaków. Nie używaj `eval`, `exec` ani `compile`.
4. Złe wejście i dzielenie przez zero mają zwracać HTTP 400 z krótkim komunikatem. Puste pole wysłane jako `?wyrazenie=` też jest błędnym wejściem; wejście na `/kalkulator` bez parametru tylko wyświetla formularz (HTTP 200). Po restarcie sprawdź: `2+3`, `7 / 2`, `-1.5*4`, `1/0` trzy wyrażenia z kroku 2 oraz puste pole.

**W raporcie:** trzy wyrażenia z kroku 2 ze skróconymi wynikami, UID procesu, tabela ośmiu testów z kodem HTTP i wynikiem po poprawce oraz jedno zdanie: dlaczego lista dozwolonych operacji jest lepsza od blokowania słów, np. `import`.

## Dodatkowo - dla chętnych, poza zakresem 90 minut

Te ćwiczenia nie są wymagane do uzyskania pełnych 3 pkt ani do raportu.

- Napisz test regresji, który po poprawkach automatycznie wysyła pięć wejść do sejfu i pięć do kalkulatora i sprawdza oczekiwane wyniki.
- W wersji podatnej spróbuj odczytać `/etc/shadow` przez kalkulator. Wyjaśnij wynik, odwołując się do UID procesu i laboratorium 5.

## Oddanie - jeden plik raportu do końca zajęć

Oddaj **jeden plik w formacie tekstowym**, np. **TXT, MD lub PDF z tekstem**. **Nazwa pliku jest dowolna. Raport należy oddać do końca zajęć** w miejscu wskazanym przez prowadzącego. Raport do jednej strony zawiera imię i nazwisko, numer indeksu, link do repozytorium GitHub, identyfikator commitu oraz wyniki i krótkie odpowiedzi z trzech zadań. Uzupełniaj go podczas pracy; oddaj również ukończone części.

W repozytorium umieść poprawioną aplikację z katalogu `aplikacja/` i README z uruchomieniem. Możesz dołączyć pliki środowiska z pakietu. Repozytorium musi być dostępne dla prowadzącego. Nie oddawaj ZIP-a, osobnych załączników z kodem ani samych zrzutów ekranu.

## Punktacja

Za każde zadanie: **0,50 pkt** za działające własne wejścia atakujące i poprawkę w repozytorium, **0,25 pkt** za wymagane wyniki w raporcie i **0,25 pkt** za poprawne wyjaśnienie. Łącznie **3 pkt**. Instalacja środowiska nie jest osobnym zadaniem punktowanym.
