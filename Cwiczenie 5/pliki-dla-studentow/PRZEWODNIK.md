# Przewodnik do laboratorium 5

## Co masz umieć po zajęciach

Rozróżnić dostęp przez HTTP od dostępu procesu do pliku, skonfigurować Basic i uzasadnić odmowę dostępu na podstawie kodu HTTP oraz praw pliku.

## Gotowość przed zajęciami

Wykonaj START.md. Sprawdź, że umiesz odczytać pełną odpowiedź GET, rozpoznać nagłówek i treść oraz policzyć prawa `640`: właściciel czyta i pisze, grupa czyta, pozostali nie mają dostępu. Przeczytaj dostarczone `httpd.conf` i `konfiguracja/dostep.conf`.

## Jak zacząć i jak rozpoznać problem

- Najpierw zapisz wynik przed zmianą. Zmieniaj jedną regułę naraz. `<Directory>` dotyczy ścieżki systemowej w kontenerze; adres URL to inna rzecz.
- `Options -Indexes` odejmuje jedną opcję. Sprawdź w dokumentacji różnicę między wyłączeniem listy a `Require all denied`.
- Basic składa się z typu, nazwy obszaru, bazy użytkowników i warunku dostępu. `AuthUserFile` wskazuje plik w kontenerze, nie na komputerze gospodarza.
- CGI musi najpierw wypisać nagłówek, potem pusty wiersz. W Pythonie efektywną tożsamość zwracają `os.geteuid()` i `os.getegid()`. Odmowę odczytu przechwyć jako wyjątek; nie przerywaj całej odpowiedzi.
- HTTP 500: sprawdź log, interpreter, LF i pustą linię. Zmiana CGI wymaga przebudowania obrazu; zmiana reguł wymaga kontroli składni i restartu.

## Punkty kontrolne

- Po zadaniu 1 umiesz wskazać przypadek, gdy katalog nie ma listy, lecz znany plik jest dostępny.
- Po zadaniu 2 błędne dane nie otwierają panelu, a publiczna strona nadal działa.
- Po zadaniu 3 potrafisz wyjaśnić wynik każdego odczytu prawami systemowymi; Basic nie zmienia UID/GID.

## Krótki raport i dowody

Na bieżąco zapisuj: wejście, oczekiwany wynik, wynik przed, wynik po i jednozdaniowy wniosek. Na pierwszej stronie podaj dane autora, repozytorium i commit, następnie trzy zwięzłe sekcje zadań. Pełne logi, ładunki i polecenia mogą być w `dowody.md` w repozytorium. Nie kopiuj tokenów ani kluczy prywatnych. Oddajesz jeden plik raportu do końca zajęć; części dodatkowe nie wpływają na pełną punktację.

Nie czekaj do końca z diagnozą problemu. Po 5 minutach bez postępu wróć do punktu kontrolnego i pokaż prowadzącemu ostatni działający krok, wejście oraz komunikat błędu.
