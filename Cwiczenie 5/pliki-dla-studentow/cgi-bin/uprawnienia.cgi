#!/usr/bin/python3
# Zadanie 3: tozsamosc procesu CGI i proba odczytu plikow z /lab-data.
import os
import sys

PLIKI = ("/lab-data/ogolny.txt", "/lab-data/poufny.txt")

wiersze = [
    "Efektywny UID: %d" % os.geteuid(),
    "Efektywny GID: %d" % os.getegid(),
    "",
]

for sciezka in PLIKI:
    try:
        with open(sciezka, encoding="utf-8") as plik:
            tresc = plik.read().rstrip("\n")
        wiersze.append("%s: odczyt OK" % sciezka)
        wiersze.append("  " + tresc)
    except PermissionError:
        wiersze.append("%s: ODMOWA ODCZYTU (PermissionError)" % sciezka)
    except OSError as blad:
        wiersze.append("%s: blad odczytu (%s)" % (sciezka, blad.strerror))

odpowiedz = "Content-Type: text/plain; charset=utf-8\r\n\r\n" + "\n".join(wiersze) + "\n"
sys.stdout.buffer.write(odpowiedz.encode("utf-8"))
