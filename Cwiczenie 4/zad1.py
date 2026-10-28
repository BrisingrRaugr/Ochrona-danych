import hashlib
import os
import sys


def sha256_pliku(sciezka):
    with open(sciezka, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def sprawdz_sumy(plik_sum):
    katalog = os.path.dirname(os.path.abspath(plik_sum))

    with open(plik_sum, "rb") as f:
        wiersze = f.read().decode("utf-8").splitlines()

    for wiersz in wiersze:
        if not wiersz.strip():
            continue  
        oczekiwany, sciezka = wiersz.split("  ", 1)
        pelna = os.path.join(katalog, sciezka)

        try:
            policzony = sha256_pliku(pelna)
        except FileNotFoundError:
            print(f"{sciezka}: BRAK")
            continue
        status = "OK" if policzony == oczekiwany.lower() else "BŁĄD"
        print(f"{sciezka}: {status}")


def roznica_bitow(a: bytes, b: bytes) -> int:
    x = int.from_bytes(a, "big") ^ int.from_bytes(b, "big")
    return bin(x).count("1")


if __name__ == "__main__":
    plik = sys.argv[1] if len(sys.argv) > 1 else "SHA256SUMS.txt"
    print("== Sprawdzanie sum kontrolnych ==")
    sprawdz_sumy(plik)

    print("\n== Efekt lawinowy ==")
    t1 = "Ala ma kota.".encode("ascii")
    t2 = "Ola ma kota.".encode("ascii")
    h1 = hashlib.sha256(t1).digest()
    h2 = hashlib.sha256(t2).digest()
    print("SHA-256('Ala ma kota.') =", h1.hex())
    print("SHA-256('Ola ma kota.') =", h2.hex())
    print("Różniące się bity:", roznica_bitow(h1, h2), "z 256")
