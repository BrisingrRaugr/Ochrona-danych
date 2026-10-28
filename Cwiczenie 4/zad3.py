import hashlib
import sys

LICZBA_WARIANTOW = 8192


def h24(dane: bytes) -> str:
    return hashlib.sha256(dane).digest()[:3].hex() 


def wczytaj_wiersze(sciezka):
    with open(sciezka, "rb") as f:
        wiersze = f.read().split(b"\n")
    assert wiersze[-1] == b"", "plik powinien kończyć się znakiem nowej linii"
    return wiersze[:-1] 


def wariant(wiersze, v: int) -> bytes:
    czesci = []
    for i, w in enumerate(wiersze):
        if (v >> i) & 1:
            czesci.append(w + b" \n")
        else:
            czesci.append(w + b"\n")
    return b"".join(czesci)


if __name__ == "__main__":
    plik_o = sys.argv[1] if len(sys.argv) > 1 else "oryginal.txt"
    plik_z = sys.argv[2] if len(sys.argv) > 2 else "zmieniony.txt"
    oryg = wczytaj_wiersze(plik_o)
    zmien = wczytaj_wiersze(plik_z)
    assert len(oryg) == 13 and len(zmien) == 13

    with open(plik_o, "rb") as f:
        assert wariant(oryg, 0) == f.read()

    slownik = {}
    for v in range(LICZBA_WARIANTOW):
        slownik.setdefault(h24(wariant(oryg, v)), v)
    print(f"Różnych h24 wśród wariantów oryginału: {len(slownik)}")

    h24_oryg0 = h24(wariant(oryg, 0))
    print(f"h24 niezmienionego oryginału: {h24_oryg0}")

    para = None
    trafienia_v0 = 0
    for v in range(LICZBA_WARIANTOW):
        s = h24(wariant(zmien, v))
        if para is None and s in slownik:
            para = (slownik[s], v, s)
        if s == h24_oryg0:
            trafienia_v0 += 1

    if para:
        vo, vz, s = para
        print(f"Para kolizyjna: v_oryginał={vo}, v_zmieniony={vz}, h24={s}")
        assert h24(wariant(oryg, vo)) == h24(wariant(zmien, vz)) == s
        assert wariant(oryg, vo) != wariant(zmien, vz)
    else:
        print("Nie znaleziono pary")

    print(f"Wariantów zmienionego z h24 = h24(oryginał v=0): {trafienia_v0}")
