"""Sejf sekretow i kalkulator - wersja po naprawie (laboratorium 7).

Zadanie 1/2: zapytanie SQL z parametrem (sqlite3 placeholder '?'), bez sklejania
napisow; uzytkownik widzi ogolny komunikat, szczegoly trafiaja do logu serwera.
Zadanie 3: kalkulator liczy wlasnym parserem (liczba operator liczba), bez eval.

Uruchamiaj wylacznie lokalnie, w kontenerze z pakietu. Dane sa fikcyjne.
"""
import re
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)
BAZA = "file:/dane/sekrety.db?mode=ro"

# Stala tresc zapytania. Wartosc klucza przekazujemy osobno, jako parametr '?'.
ZAPYTANIE_SEKRET = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"

# Liczba: opcjonalny minus, czesc calkowita, opcjonalna czesc dziesietna.
LICZBA = r"-?\d+(?:\.\d+)?"
# Dozwolona gramatyka: liczba, operator, liczba; dopuszczalne spacje wokol operatora.
WYRAZENIE = re.compile(rf"\s*({LICZBA})\s*([+\-*/])\s*({LICZBA})\s*")
DZIALANIA = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def na_liczbe(tekst):
    """Zamienia dopasowany fragment na int lub float."""
    return float(tekst) if "." in tekst else int(tekst)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sekret")
def sekret():
    klucz = request.args.get("klucz", "")
    wiersze, blad = [], None
    try:
        with sqlite3.connect(BAZA, uri=True) as db:
            # Tresc zapytania jest stala; (klucz,) to jednoelementowa krotka wartosci.
            wiersze = db.execute(ZAPYTANIE_SEKRET, (klucz,)).fetchall()
    except sqlite3.Error:
        # Uzytkownik dostaje ogolny komunikat; szczegoly trafiaja tylko do logu.
        app.logger.exception("Blad zapytania w /sekret")
        blad = "Wystapil blad podczas obslugi zapytania."
    # W trybie diagnostycznym pokazujemy stala tresc zapytania i wartosc parametru osobno.
    zapytanie = f"{ZAPYTANIE_SEKRET}    -- parametr: {klucz!r}"
    return render_template("sekret.html", klucz=klucz, zapytanie=zapytanie, wiersze=wiersze, blad=blad)


@app.route("/kalkulator")
def kalkulator():
    # Brak parametru 'wyrazenie' -> tylko formularz (HTTP 200).
    if "wyrazenie" not in request.args:
        return render_template("kalkulator.html", wyrazenie="", wynik=None)

    wyrazenie = request.args.get("wyrazenie", "")

    # Limit dlugosci wejscia.
    if len(wyrazenie) > 100:
        return "Nieprawidlowe dane: wejscie jest za dlugie.", 400

    # Cale wejscie musi pasowac do gramatyki: liczba operator liczba.
    dopasowanie = WYRAZENIE.fullmatch(wyrazenie)
    if dopasowanie is None:
        return "Nieprawidlowe dane: dozwolone jest 'liczba operator liczba'.", 400

    a = na_liczbe(dopasowanie.group(1))
    operator = dopasowanie.group(2)
    b = na_liczbe(dopasowanie.group(3))

    if operator == "/" and b == 0:
        return "Nieprawidlowe dane: dzielenie przez zero.", 400

    wynik = DZIALANIA[operator](a, b)
    return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik=wynik)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
