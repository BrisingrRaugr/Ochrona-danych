# Dowody – Laboratorium 5

Hasło i zawartość `auth/uzytkownicy` celowo pominięte. Wpisy logów skopiowane w całości z `docker compose logs --no-log-prefix web`.

## Zadanie 1

Przed zmianą `/materialy/` i `/wewnetrzne/` zwracały `200 OK` z treścią `Index of /materialy` / `Index of /wewnetrzne`; oba pliki `200 OK`.

Po zmianie (`curl.exe -i`):


GET /materialy/            -> HTTP/1.1 403 Forbidden
GET /materialy/notatka.txt -> HTTP/1.1 200 OK  "Publiczna notatka: ten plik ma pozostac dostepny pod znanym adresem."
GET /wewnetrzne/           -> HTTP/1.1 403 Forbidden
GET /wewnetrzne/plan.txt   -> HTTP/1.1 403 Forbidden


Log:


[Wed Nov 04 11:36:23.569622 2026] [autoindex:error] [pid 11:tid 39] [client 172.18.0.1:51452] AH01276: Cannot serve directory /usr/local/apache2/htdocs/materialy/: No matching DirectoryIndex (index.html) found, and server-generated directory index forbidden by Options directive
172.18.0.1 - - [04/Nov/2026:11:36:23 +0000] "GET /materialy/ HTTP/1.1" 403 239
172.18.0.1 - - [04/Nov/2026:11:38:21 +0000] "GET /materialy/notatka.txt HTTP/1.1" 200 69
[Wed Nov 04 12:05:05.194947 2026] [authz_core:error] [pid 13:tid 41] [client 172.18.0.1:54018] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/
172.18.0.1 - - [04/Nov/2026:12:05:05 +0000] "GET /wewnetrzne/ HTTP/1.1" 403 239
[Wed Nov 04 12:05:05.312351 2026] [authz_core:error] [pid 13:tid 48] [client 172.18.0.1:54022] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/plan.txt
172.18.0.1 - - [04/Nov/2026:12:05:05 +0000] "GET /wewnetrzne/plan.txt HTTP/1.1" 403 239


## Zadanie 2


docker compose run --rm --no-deps narzedzia -cB /auth/uzytkownicy student


Bez logowania:


HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Laboratorium 5"


Log (bez logowania, błędne hasło, poprawne hasło, strona publiczna):


172.18.0.1 - - [04/Nov/2026:11:55:15 +0000] "GET /panel/raport.txt HTTP/1.1" 401 421
172.18.0.1 - student [04/Nov/2026:11:55:22 +0000] "GET /panel/raport.txt HTTP/1.1" 401 421
[Wed Nov 04 11:55:22.621424 2026] [auth_basic:error] [pid 13:tid 36] [client 172.18.0.1:50560] AH01617: user student: authentication failure for "/panel/raport.txt": Password Mismatch
172.18.0.1 - student [04/Nov/2026:11:55:26 +0000] "GET /panel/raport.txt HTTP/1.1" 200 58
172.18.0.1 - - [04/Nov/2026:11:55:26 +0000] "GET / HTTP/1.1" 200 351


## Zadanie 3


$ docker compose exec web ls -ln /lab-data/
-rw-r-----    1 0        2               48 Nov  4 08:30 ogolny.txt
-rw-------    1 0        2               61 Nov  4 08:30 poufny.txt
$ docker compose exec web id daemon
uid=2(daemon) gid=2(daemon) groups=2(daemon),1(bin),2(daemon),4(adm)


Odpowiedź CGI (taka sama przed Basic i po zalogowaniu):


HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

Efektywny UID: 2
Efektywny GID: 2

/lab-data/ogolny.txt: odczyt OK
  LAB05: dokument dostepny dla grupy procesu WWW.
/lab-data/poufny.txt: ODMOWA ODCZYTU (PermissionError)


Log (przed Basic, po Basic bez logowania, po Basic z poprawnym hasłem):


172.18.0.1 - - [04/Nov/2026:12:00:38 +0000] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 200 172
172.18.0.1 - - [04/Nov/2026:12:01:25 +0000] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 401 421
172.18.0.1 - student [04/Nov/2026:12:01:42 +0000] "GET /cgi-bin/uprawnienia.cgi HTTP/1.1" 200 172

