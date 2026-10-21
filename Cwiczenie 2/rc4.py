import math
import string
import sys
import time
from collections import Counter
from itertools import product
 
 
def rc4(klucz: bytes, dane: bytes) -> bytes:
    """KSA + PRGA + XOR. Każde wywołanie zaczyna od nowego stanu."""
    # KSA
    S = list(range(256))
    j = 0
    n = len(klucz)
    for i in range(256):
        j = (j + S[i] + klucz[i % n]) % 256
        S[i], S[j] = S[j], S[i]
    # PRGA + XOR
    wynik = bytearray(len(dane))
    i = j = 0
    for idx, b in enumerate(dane):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        wynik[idx] = b ^ S[(S[i] + S[j]) % 256]
    return bytes(wynik)
 
 
def entropia(dane: bytes) -> float:
    """Entropia Shannona histogramu bajtów [bit/bajt]."""
    if not dane:
        return 0.0
    n = len(dane)
    return -sum(c / n * math.log2(c / n) for c in Counter(dane).values())
 
 
def testy():
    print("== Testy RC4 ==")
    # wektory testowe RC4 (Wikipedia / RFC 6229)
    wektory = [
        (b"Key", b"Plaintext", "bbf316e8d940af0ad3"),
        (b"Wiki", b"pedia", "1021bf0420"),
        (b"Secret", b"Attack at dawn", "45a01f645fc35b383552544b9bf5"),
    ]
    for k, p, oczek in wektory:
        c = rc4(k, p)
        print(f"rc4({k!r}, {p!r}) = {c.hex()}  {'OK' if c.hex() == oczek else 'BŁĄD'}")
    # dwukrotne zastosowanie odtwarza wejście
    d = bytes(range(256)) * 3
    print("rc4(k, rc4(k, x)) == x:", rc4(b"abc", rc4(b"abc", d)) == d)
    print("puste dane:", rc4(b"abc", b"") == b"")
    print()
 
 
def main():
    if len(sys.argv) != 2:
        print("Użycie: python rc4.py rc4.bin")
        sys.exit(1)
 
    testy()
 
    with open(sys.argv[1], "rb") as f:
        krypto = f.read()
    print(f"Rozmiar kryptogramu: {len(krypto)} B")
    print("Początek kryptogramu:", repr(krypto[:50]))
 
    # 3.2 - pełne przeszukanie przestrzeni kluczy aaa..zzz
    probka = krypto[:512]
    ranking = []
    t0 = time.perf_counter()
    for litery in product(string.ascii_lowercase, repeat=3):
        k = "".join(litery).encode("ascii")
        ranking.append((entropia(rc4(k, probka)), k))
    czas = time.perf_counter() - t0
    proby = len(ranking)
 
    # entropia rosnąco, remisy alfabetycznie
    ranking.sort(key=lambda r: (r[0], r[1]))
    print(f"\nSprawdzono {proby} kluczy w {czas:.2f} s")
    print("Pięciu najlepszych kandydatów (entropia pierwszych 512 B):")
    for nr, (h, k) in enumerate(ranking[:5], 1):
        podglad = rc4(k, krypto[:40])
        print(f"{nr}. {k.decode()}  H={h:.4f}  {podglad!r}")
 
    klucz = ranking[0][1]  # wybór automatyczny
    print(f"\nWybrany klucz: {klucz.decode()}")
 
    # 3.3 - pełne odszyfrowanie od nowego stanu
    jawny = rc4(klucz, krypto)
    with open("rc4.txt", "wb") as f:
        f.write(jawny)
    print(f"Zapisano rc4.txt ({len(jawny)} B)")
    print("Początek odszyfrowania:", repr(jawny[:120]))
 
    drukowalne = sum(1 for b in jawny if 32 <= b <= 126 or b in (9, 10, 13))
    print(f"Udział drukowalnych ASCII: {drukowalne / len(jawny):.4f}")
    print("Ponowne szyfrowanie == kryptogram:", rc4(klucz, jawny) == krypto)
 
    print(f"\nEntropia kryptogramu:     {entropia(krypto):.4f} bit/B")
    print(f"Entropia odszyfrowania:   {entropia(jawny):.4f} bit/B")
 
 
if __name__ == "__main__":
    main()