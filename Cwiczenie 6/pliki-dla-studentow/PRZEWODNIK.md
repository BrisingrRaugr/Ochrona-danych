# Przewodnik do laboratorium 6

## Co masz umieć po zajęciach

Prześledzić wejście od użytkownika do miejsca interpretacji HTML/JavaScript, odtworzyć trzy odmiany XSS i sprawdzić, czy naprawa zachowuje działanie aplikacji.

## Kontrola na początku zajęć

Wykonaj START.md i otwórz DevTools: Network, Console oraz Cookies. Używaj dwóch odrębnych sesji: zwykłe okno i prywatne. Dwa okna prywatne tej samej przeglądarki zwykle współdzielą ciasteczka. Aplikację otwieraj przez `127.0.0.1`, zbieracz przez `localhost`.

## Pojęcia i wskazówki

- Odbity/zapisany opisuje drogę danych; DOM opisuje miejsce powstania podatności. Te kategorie nie muszą się wykluczać. W ćwiczeniu badamy trzy konkretne ścieżki.
- URL zakoduj, np. przez `encodeURIComponent` dla wartości parametru. Znak `&` rozdziela parametry, a `#` zaczyna fragment niewysyłany do serwera.
- Kodowanie HTML chroni w kontekście tekstu HTML. Nie jest uniwersalnym sposobem zabezpieczenia JavaScript, CSS ani schematów URL. Atrybuty HTML muszą być ujęte w cudzysłowy.
- `document.cookie` zwraca tylko ciasteczka dostępne skryptowi. Przed przesłaniem ich jako wartości parametru zakoduj cały tekst. Aby użyć tokenu w curl, odkoduj wartość parametru z logu URL.
- Po włączeniu HttpOnly zaloguj się ponownie; sam restart nie zmienia istniejącego ciasteczka. Skradziony wcześniej token pozostaje ważny. HttpOnly nie zabrania skryptowi wysyłania żądań z sesją ofiary.
- Po restarcie ogłoszenia znikają. Przed powtórką dodaj ładunek ponownie. Po przeniesieniu skryptu do pliku odśwież bez pamięci podręcznej. `after_request` musi zwrócić obiekt odpowiedzi.

## Punkty kontrolne

- Zadanie 1: zapisany ten sam URL przed i po; wyszukiwarka nadal znajduje zwykłe słowo.
- Zadanie 2: notatka konta Anny odczytana skopiowanym tokenem; po nowym logowaniu skrypt nie czyta nowego ciasteczka HttpOnly.
- Zadanie 3: brak wykonania trzech ładunków oraz działający podgląd zwykłego tekstu. Sam brak efektu ataku przy zepsutej stronie nie wystarcza.

Hasła i klucz podpisu w aplikacji są jawne ćwiczeniowo. Poprawienie XSS nie stanowi pełnego audytu aplikacji do wdrożenia.

## Krótki raport i dowody

Na bieżąco zapisuj: wejście, oczekiwany wynik, wynik przed, wynik po i jednozdaniowy wniosek. Na pierwszej stronie podaj dane autora, repozytorium i commit, następnie trzy zwięzłe sekcje zadań. Pełne logi, ładunki i polecenia mogą być w `dowody.md` w repozytorium. Nie kopiuj tokenów ani kluczy prywatnych. Oddajesz jeden plik raportu do końca zajęć; części dodatkowe nie wpływają na pełną punktację.

Nie czekaj do końca z diagnozą problemu. Po 5 minutach bez postępu wróć do punktu kontrolnego i pokaż prowadzącemu ostatni działający krok, wejście oraz komunikat błędu.
