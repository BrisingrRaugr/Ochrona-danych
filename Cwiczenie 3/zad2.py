from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

PASSWORD = "testowe-haslo-lab3"
ITERATIONS = 200_000
KEY_LEN = 32
SALT_LEN = 16
IV_LEN = 16


def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password.encode("utf-8"), salt, dkLen=KEY_LEN,
                  count=ITERATIONS, hmac_hash_module=SHA256)


def encrypt(password: str, plaintext: bytes):
    salt = get_random_bytes(SALT_LEN)
    iv = get_random_bytes(IV_LEN)
    key = derive_key(password, salt)
    ct = AES.new(key, AES.MODE_CBC, iv=iv).encrypt(pad(plaintext, AES.block_size, style="pkcs7"))
    return salt, iv, ct           


def decrypt(password: str, salt: bytes, iv: bytes, ct: bytes) -> bytes:
    key = derive_key(password, salt)      
    padded = AES.new(key, AES.MODE_CBC, iv=iv).decrypt(ct)
    return unpad(padded, AES.block_size, style="pkcs7")


def expected_len(n: int) -> int:
    return (n // 16 + 1) * 16


def test(name: str, data: bytes):
    salt, iv, ct = encrypt(PASSWORD, data)
    out = decrypt(PASSWORD, salt, iv, ct)
    ok_bytes = out == data
    ok_len = len(ct) == expected_len(len(data))
    print(f"[{'OK' if ok_bytes and ok_len else 'BŁĄD'}] {name}: wejście {len(data)} B, "
          f"kryptogram {len(ct)} B (oczekiwane {expected_len(len(data))}), bajty równe: {ok_bytes}")
    assert ok_bytes and ok_len


with open("wiadomosc.txt", "rb") as f:
    message = f.read()

test("puste dane", b"")
test("16 B ASCII", b"0123456789ABCDEF")
test("wiadomosc.txt", message)

s1, iv1, c1 = encrypt(PASSWORD, message)
s2, iv2, c2 = encrypt(PASSWORD, message)
print("\nDwa szyfrowania wiadomości tym samym hasłem:")
print("  sól 1:", s1.hex(), " IV 1:", iv1.hex())
print("  sól 2:", s2.hex(), " IV 2:", iv2.hex())
print("  kryptogram 1 (początek):", c1[:16].hex())
print("  kryptogram 2 (początek):", c2[:16].hex())
print("  kryptogramy identyczne:", c1 == c2)
print("  oba odszyfrowują się poprawnie:",
      decrypt(PASSWORD, s1, iv1, c1) == message and decrypt(PASSWORD, s2, iv2, c2) == message)
