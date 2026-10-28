import hashlib
import hmac
import secrets
import sys

ITERACJE_NOWE = 600000
DLUGOSC_SOLI = 16
DLUGOSC_SKROTU = 32 


def wczytaj_baze(sciezka):

    baza = {}
    with open(sciezka, "rb") as f:
        for wiersz in f.read().decode("utf-8").splitlines():
            if not wiersz.strip():
                continue
            login, iteracje, sol_hex, skrot_hex = wiersz.split(":")
            baza[login] = (int(iteracje), bytes.fromhex(sol_hex), bytes.fromhex(skrot_hex))
    return baza


def pbkdf2(haslo: str, sol: bytes, iteracje: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", haslo.encode("utf-8"), sol, iteracje, DLUGOSC_SKROTU)


def weryfikuj(baza, login, haslo) -> bool:
    rekord = baza.get(login)
    if rekord is None:
        return False
    iteracje, sol, zapisany = rekord
    policzony = pbkdf2(haslo, sol, iteracje)
    return hmac.compare_digest(policzony, zapisany)


def dodaj(baza, login, haslo) -> str:
    sol = secrets.token_bytes(DLUGOSC_SOLI)
    skrot = pbkdf2(haslo, sol, ITERACJE_NOWE)
    baza[login] = (ITERACJE_NOWE, sol, skrot)
    return f"{login}:{ITERACJE_NOWE}:{sol.hex()}:{skrot.hex()}"


if __name__ == "__main__":
    plik = sys.argv[1] if len(sys.argv) > 1 else "hasla.txt"
    baza = wczytaj_baze(plik)

    print("== Testy weryfikacji ==")
    testy = [
        ("anna", "Kasztan-2026"),
        ("anna", "kasztan-2026"),
        ("piotr", "Żółw na łące"), 
        ("kasia", "Kasztan-2026"),
    ]
    for login, haslo in testy:
        print(f"weryfikuj({login!r}, {haslo!r}) -> {weryfikuj(baza, login, haslo)}")

    print("\n== Nowe konta z tym samym hasłem ==")
    wspolne = "Wspolne-Haslo-123"
    dodaj(baza, "test1", wspolne)
    dodaj(baza, "test2", wspolne)
    _, sol1, skrot1 = baza["test1"]
    _, sol2, skrot2 = baza["test2"]
    print("Sole równe:  ", sol1 == sol2)
    print("Skróty równe:", skrot1 == skrot2)
    print("weryfikuj(test1):", weryfikuj(baza, "test1", wspolne))
    print("weryfikuj(test2):", weryfikuj(baza, "test2", wspolne))
