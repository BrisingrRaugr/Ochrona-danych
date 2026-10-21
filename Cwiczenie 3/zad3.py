import math
from collections import Counter
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"
SAMPLE = 4096


def decrypt_raw(key: bytes, data: bytes) -> bytes:
    return AES.new(key, AES.MODE_ECB).decrypt(data)


def entropy(data: bytes) -> float:
    n = len(data)
    counts = Counter(data)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


with open("slaby_ecb.bin", "rb") as f:
    ct = f.read()

sample = ct[:SAMPLE]
candidates = []
for ch in ALPHABET:
    key = (ch * 16).encode("ascii")
    candidates.append((entropy(decrypt_raw(key, sample)), ch))

candidates.sort()
print("Pięciu najlepszych kandydatów (najniższa entropia):")
for h, ch in candidates[:5]:
    print(f"  '{ch}'  H = {h:.4f}")

best_h, best = candidates[0]
plain = unpad(decrypt_raw((best * 16).encode("ascii"), ct), AES.block_size, style="pkcs7")
text = plain.decode("utf-8")
print(f"\nOdzyskany znak klucza: '{best}'")
print("Pierwszy wiersz:", text.splitlines()[0])
print("\nPoczątek tekstu:\n" + text[:400])
