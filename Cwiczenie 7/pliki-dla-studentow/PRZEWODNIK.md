# Przewodnik do laboratorium 7

## Co masz umieć po zajęciach

Wyjaśnić, gdzie dane stały się kodem, odróżnić parametryzację od walidacji i zbudować parser dopuszczający wyłącznie opisaną gramatykę.

## Kontrola na początku zajęć

Wykonaj START.md. Przeczytaj `app.py`. Na małym przykładzie sqlite3 sprawdź przekazanie jednej wartości w krotce `(wartosc,)`; przecinek ma znaczenie. Przećwicz `re.fullmatch` na wzorcu cyfr.

## Wskazówki

- Zapisz zapytanie SQL po podstawieniu swojego wejścia i zaznacz, gdzie kończy się literał. Do pierwszego UNION dobierz liczbę kolumn zgodną z zapytaniem aplikacji. W `sqlite_master` kolumna `sql` zawiera opis utworzenia tabeli.
- Zestaw bazowy to pięć wejść: legalny klucz, apostrof, zawsze prawdziwy warunek, UNION schematu i UNION drugiej tabeli. Po naprawie dochodzi szósty: legalny klucz z apostrofem.
- Przy parametryzacji przekazuj niezmienny SQL i wartości osobno. Nie wstawiaj apostrofów wokół `?` ani nie formatuj wartości przed `execute`.
- Parametr zastępuje wartość, nie nazwę tabeli. Jeśli aplikacja wybiera nazwę tabeli, wybór musi pochodzić z ustalonej listy w kodzie.
- Parser kalkulatora rozbij na: limit długości, dopasowanie całego napisu, zamianę dwóch liczb, wybór działania ze słownika i obsługę dzielenia przez zero. Nie obliczaj wejścia interpreterem.
- `+` w URL bywa zamieniany na spację. Użyj formularza albo `curl -G --data-urlencode "wyrazenie=2+3" http://127.0.0.1:8080/kalkulator` (Windows: `curl.exe`).

## Punkty kontrolne

- Przed naprawą znasz liczbę wierszy dla każdego z pięciu wejść.
- Po parametryzacji oba legalne klucze działają, ataki nie zwracają cudzych danych.
- Po naprawie kalkulatora działają liczby ujemne i ułamki, a kod Pythona, puste pole i dzielenie przez zero są odrzucane. Dodatkowo sprawdź `2+3abc` i 101 znaków.

Tryb diagnostyczny pozostaje na potrzeby zajęć. Parametryzacja nie zastępuje uprawnień użytkownika, a sam zakaz zapisu w kontenerze nie usuwa Code Injection.

## Krótki raport i dowody

Na bieżąco zapisuj: wejście, oczekiwany wynik, wynik przed, wynik po i jednozdaniowy wniosek. Na pierwszej stronie podaj dane autora, repozytorium i commit, następnie trzy zwięzłe sekcje zadań. Pełne logi, ładunki i polecenia mogą być w `dowody.md` w repozytorium. Nie kopiuj tokenów ani kluczy prywatnych. Oddajesz jeden plik raportu do końca zajęć; części dodatkowe nie wpływają na pełną punktację.

Nie czekaj do końca z diagnozą problemu. Po 5 minutach bez postępu wróć do punktu kontrolnego i pokaż prowadzącemu ostatni działający krok, wejście oraz komunikat błędu.
