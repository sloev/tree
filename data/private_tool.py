"""Krypterede private personer (nulevende / født inden for 100 år uden dødsdato).

De fulde oplysninger ligger AES-256-GCM-krypteret i data/private.enc (nøgle: PBKDF2-SHA256 af kodeordet,
200.000 iterationer). Siden dekrypterer i browseren med samme parametre. Kodeordet gemmes ikke i repoet.

  FAMILY_PASSWORD=... python3 data/private_tool.py decrypt   # skriver data/private_people.json (gitignored)
  FAMILY_PASSWORD=... python3 data/private_tool.py encrypt   # krypterer data/private_people.json -> data/private.enc
                                                             # og skriver data/private_stubs.json (uden navne)
"""
import base64, json, os, sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HERE = os.path.dirname(os.path.abspath(__file__))
ENC, PLAIN, STUBS = (os.path.join(HERE, f) for f in ("private.enc", "private_people.json", "private_stubs.json"))
ITER = 200_000
STUB_KEYS = ("id", "sex", "ahnen", "line", "rel", "father", "mother", "sibof", "step", "spouse")

def key(pw, salt):
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pw.encode("utf-8"))

def encrypt(obj, pw):
    salt, iv = os.urandom(16), os.urandom(12)
    ct = AESGCM(key(pw, salt)).encrypt(iv, json.dumps(obj, ensure_ascii=False).encode("utf-8"), None)
    b = lambda x: base64.b64encode(x).decode()
    return {"v": 1, "kdf": "PBKDF2-SHA256", "iter": ITER, "salt": b(salt), "iv": b(iv), "ct": b(ct)}

def decrypt(blob, pw):
    d = lambda k: base64.b64decode(blob[k])
    return json.loads(AESGCM(key(pw, d("salt"))).decrypt(d("iv"), d("ct"), None))

def stub(p):
    s = {k: p.get(k) for k in STUB_KEYS}
    s.update(name="Privat person", private=True, living=True, conf="told", born=None, bplace=None, died=None, dplace=None,
             occ=[], note=None, src=[], res=[])
    return s

if __name__ == "__main__":
    pw = os.environ.get("FAMILY_PASSWORD") or sys.exit("Sæt FAMILY_PASSWORD")
    if sys.argv[1] == "decrypt":
        json.dump(decrypt(json.load(open(ENC)), pw), open(PLAIN, "w"), ensure_ascii=False, indent=1)
        print("skrev", PLAIN)
    elif sys.argv[1] == "encrypt":
        people = json.load(open(PLAIN))
        json.dump(encrypt(people, pw), open(ENC, "w"))
        json.dump([stub(p) for p in people if not p.get("patch")], open(STUBS, "w"), ensure_ascii=False, indent=1)
        print(len(people), "private personer krypteret")
