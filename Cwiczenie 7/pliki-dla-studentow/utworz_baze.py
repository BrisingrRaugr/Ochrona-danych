"""Tworzy fikcyjna baze sekretow podczas budowy obrazu."""
import sqlite3
import sys

with sqlite3.connect(sys.argv[1]) as db:
    db.execute("CREATE TABLE sekrety(klucz TEXT, wlasciciel TEXT, sekret TEXT)")
    db.executemany("INSERT INTO sekrety VALUES (?, ?, ?)", [
        ("1234", "anna", "Hello world"),
        ("qwerty", "piotr", "Top secret"),
        ("d'Artagnan", "muszkieter", "Jeden za wszystkich"),
        ("K7-ZQ19", "admin", "Szyfr do sejfu: 7319 (fikcyjny)"),
    ])
    db.execute("CREATE TABLE konta(login TEXT, rola TEXT, email TEXT)")
    db.executemany("INSERT INTO konta VALUES (?, ?, ?)", [
        ("anna", "uzytkownik", "anna@lab7.example"),
        ("admin", "administrator", "admin@lab7.example"),
    ])
