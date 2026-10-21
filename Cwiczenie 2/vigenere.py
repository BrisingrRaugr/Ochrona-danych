import sys
 
 
def szyfruj(dane: bytes, klucz: bytes) -> bytes:
    if not klucz:
        raise ValueError("Klucz nie może być pusty")
    m = len(klucz)
    return bytes((p + klucz[i % m]) % 256 for i, p in enumerate(dane))
 
 
def odszyfruj(dane: bytes, klucz: bytes) -> bytes:
    if not klucz:
        raise ValueError("Klucz nie może być pusty")
    m = len(klucz)
    return bytes((c - klucz[i % m]) % 256 for i, c in enumerate(dane))
 
 
def podziel_hex(dane: bytes, n: int = 5) -> str:
    return " | ".join(dane[i:i + n].hex() for i in range(0, len(dane), n))
 
 
def testy():
    print("== Testy ==")
    # puste dane
    assert szyfruj(b"", b"ZAMEK") == b""
    assert odszyfruj(b"", b"ZAMEK") == b""
    print("puste dane: OK")
 
    # bajty 0 i 255 (zawijanie modulo 256 w obie strony)
    d = bytes([0, 255, 0, 255, 128, 1, 254])
    for klucz in (b"ZAMEK", bytes([255]), bytes([0, 1, 255])):
        c = szyfruj(d, klucz)
        assert odszyfruj(c, klucz) == d
    print("bajty 0 i 255:", repr(d), "->", repr(szyfruj(d, b"ZAMEK")), "-> OK")
 
    # wszystkie wartości bajtów
    d = bytes(range(256))
    assert odszyfruj(szyfruj(d, b"ZAMEK"), b"ZAMEK") == d
    print("wszystkie bajty 0..255: OK")
 
    # pusty klucz jest odrzucany
    try:
        szyfruj(b"abc", b"")
        print("pusty klucz: BŁĄD (brak wyjątku)")
    except ValueError:
        print("pusty klucz: odrzucony (ValueError) - OK")
 
 
def main():
    if len(sys.argv) != 2:
        print("Użycie: python vigenere.py tekst_pl.txt")
        sys.exit(1)
    sciezka = sys.argv[1]
 
    # 2.1 - szyfrowanie pliku kluczem ZAMEK
    with open(sciezka, "rb") as f:
        zrodlo = f.read()
    klucz = b"ZAMEK"
    krypto = szyfruj(zrodlo, klucz)
    with open("vigenere.bin", "wb") as f:
        f.write(krypto)
    print(f"Zaszyfrowano {len(zrodlo)} B kluczem {klucz!r} -> vigenere.bin")
    print("Początek kryptogramu:", repr(krypto[:50]))
 
    with open("vigenere.bin", "rb") as f:
        odczyt = f.read()
    jawny = odszyfruj(odczyt, klucz)
    zgodne = jawny == zrodlo
    print(f"Odszyfrowanie zgodne ze źródłem bajt po bajcie: {zgodne}")
    if not zgodne:
        roznice = sum(a != b for a, b in zip(jawny, zrodlo))
        print(f"  różne bajty: {roznice}, długości: {len(jawny)} / {len(zrodlo)}")
    print("Początek odszyfrowania:", jawny[:60].decode("utf-8", errors="replace"))
    print()
 
    testy()
    print()
 
    # 2.2 - powtarzany tekst a długość klucza
    tekst = b"BRAMABRAMABRAMA"
    print("== Tekst", tekst.decode(), "(okres 5) ==")
    for k in (b"SZYFR", b"KOD"):
        c = szyfruj(tekst, k)
        assert odszyfruj(c, k) == tekst
        print(f"klucz {k.decode():5s} (m={len(k)}): {podziel_hex(c)}")
 
 
if __name__ == "__main__":
    main()