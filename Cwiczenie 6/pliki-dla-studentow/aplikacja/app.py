"""Tablica ogloszen - celowo podatna aplikacja do laboratorium 6.

Uruchamiaj wylacznie lokalnie, w kontenerze z pakietu. Konta i dane sa fikcyjne.
"""
from flask import Flask, redirect, render_template, request, session, url_for
from html import escape

app = Flask(__name__)
app.secret_key = "lab6-cwiczeniowy-klucz-nie-do-produkcji"
app.config["SESSION_COOKIE_HTTPONLY"] = True

UZYTKOWNICY = {"anna": "anna-lab6", "student": "student-lab6"}
NOTATKI = {
    "anna": "Prywatna notatka Anny: kod do szafki w pracowni 4721 (fikcyjny).",
    "student": "Prywatna notatka studenta: dokończyć raport z laboratorium 6.",
}
WPISY = [("anna", "Witajcie na tablicy ogłoszeń! Konsultacje w piątek o 12:00.")]


@app.route("/")
def tablica():
    return render_template("tablica.html", wpisy=WPISY, uzytkownik=session.get("uzytkownik"))


@app.post("/dodaj")
def dodaj():
    if "uzytkownik" not in session:
        return redirect(url_for("logowanie"))
    WPISY.append((session["uzytkownik"], request.form.get("tresc", "")[:2000]))
    return redirect(url_for("tablica"))


@app.route("/szukaj")
def szukaj():
    fraza = request.args.get("q", "")
    html = "<!doctype html><meta charset='utf-8'><title>Szukaj</title>"
    html += "<h1>Wyniki wyszukiwania dla: " + escape(fraza) + "</h1><ul>"
    for autor, tresc in WPISY:
        if fraza.lower() in tresc.lower():
            html += "<li>" + escape(autor) + ": " + escape(tresc) + "</li>"
    return html + "</ul><p><a href='/'>Powrót</a></p>"


@app.route("/podglad")
def podglad():
    return render_template("podglad.html")


@app.route("/logowanie", methods=["GET", "POST"])
def logowanie():
    blad = None
    if request.method == "POST":
        login = request.form.get("login", "")
        if UZYTKOWNICY.get(login) == request.form.get("haslo"):
            session["uzytkownik"] = login
            return redirect(url_for("tablica"))
        blad = "Błędny login lub hasło."
    return render_template("logowanie.html", blad=blad)


@app.route("/notatka")
def notatka():
    if "uzytkownik" not in session:
        return redirect(url_for("logowanie"))
    return render_template("notatka.html", uzytkownik=session["uzytkownik"],
                           notatka=NOTATKI[session["uzytkownik"]])


@app.route("/wyloguj")
def wyloguj():
    session.clear()
    return redirect(url_for("tablica"))


@app.after_request
def dodaj_csp(odpowiedz):
    odpowiedz.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'"
    )
    return odpowiedz


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
