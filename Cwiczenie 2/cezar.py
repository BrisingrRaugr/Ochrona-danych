import sys

DOZWOLONE = set(range(32, 127)) | {9, 10, 13}


def odszyfruj(dane: bytes, k: int) -> bytes:
    return bytes((c - k) % 256 for c in dane)


def ocena(tekst: bytes) -> float:
    if not tekst:
        return 0.0
    return sum(1 for b in tekst if b in DOZWOLONE) / len(tekst)


def main():
    # bez argumentu domyślnie cezar.bin
    sciezka = sys.argv[1] if len(sys.argv) > 1 else "cezar.bin"

    with open(sciezka, "rb") as f:
        dane = f.read()
    print(f"Rozmiar kryptogramu: {len(dane)} B")
    print("Początek kryptogramu:", repr(dane[:50]))

    wyniki = []
    for k in range(256):
        jawny = odszyfruj(dane, k)
        wyniki.append((ocena(jawny), k, jawny))

    # ocena malejąco, remisy rosnąco według k
    wyniki.sort(key=lambda w: (-w[0], w[1]))
    top5 = wyniki[:5]

    print("\nPięciu najlepszych kandydatów:")
    for nr, (o, k, jawny) in enumerate(top5, 1):
        print(f"{nr}. k={k:3d}  ocena={o:.4f}  {jawny[:60]!r}")

    # wybór: numer 1-5 albo k=<liczba>
    wybor = input("\nWybierz numer [1-5] lub podaj k=<0..255>: ").strip()
    if wybor.lower().startswith("k="):
        k = int(wybor[2:]) % 256
        jawny = odszyfruj(dane, k)
    else:
        nr = int(wybor) if wybor else 1
        _, k, jawny = top5[nr - 1]

    with open("cezar.txt", "wb") as f:
        f.write(jawny)
    print(f"Wybrano k={k}. Zapisano cezar.txt")


if __name__ == "__main__":
    main()