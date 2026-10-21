from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK = 16
data = b"0123456789ABCDEF" * 4                          
key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")  
iv = get_random_bytes(16)                                


def blocks(b):
    return [b[i:i + BLOCK] for i in range(0, len(b), BLOCK)]


def report(name, ct):
    bl = blocks(ct)
    print(f"--- {name} ---")
    for i, blk in enumerate(bl, 1):
        print(f"  blok {i}: {blk.hex()}")
    equal = [(i + 1, j + 1) for i in range(len(bl)) for j in range(i + 1, len(bl)) if bl[i] == bl[j]]
    print("  równe pary bloków:", equal if equal else "brak")

ct_ecb = AES.new(key, AES.MODE_ECB).encrypt(data)
ct_cbc = AES.new(key, AES.MODE_CBC, iv=iv).encrypt(data)

print("IV (CBC):", iv.hex())
report("ECB", ct_ecb)
report("CBC", ct_cbc)

pt_ecb = AES.new(key, AES.MODE_ECB).decrypt(ct_ecb)
pt_cbc = AES.new(key, AES.MODE_CBC, iv=iv).decrypt(ct_cbc)
print("ECB: odszyfrowane == wejście:", pt_ecb == data)
print("CBC: odszyfrowane == wejście:", pt_cbc == data)
