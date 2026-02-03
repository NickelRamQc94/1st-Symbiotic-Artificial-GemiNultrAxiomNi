#!/usr/bin/env python3
# sign/verify blobs with Ed25519 (PyNaCl)
import argparse, sys, base64, json, hashlib, os

try:
    from nacl.signing import SigningKey, VerifyKey
    from nacl.exceptions import BadSignatureError
except Exception:
    print("PyNaCl required. Install: pip install pynacl", file=sys.stderr); sys.exit(2)

# --- COULEURS CLI ---
class C:
    OK = '\033[92m'
    FAIL = '\033[91m'
    END = '\033[0m'
    
def sha256_bytes(path):
    h = hashlib.sha256(); 
    with open(path,'rb') as f:
        for ch in iter(lambda: f.read(65536), b''): h.update(ch)
    return h.digest()

def genkey(out_sk="ed25519_sk.bin", out_vk="ed25519_vk.b64"):
    sk = SigningKey.generate()
    vk = sk.verify_key
    with open(out_sk,"wb") as f: f.write(sk.encode())
    with open(out_vk,"wb") as f: f.write(base64.b64encode(vk.encode()))
    print("Keys written:", out_sk, out_vk)

def sign(path, sk_path, out_sig=None, meta=None):
    with open(sk_path,"rb") as f: sk = SigningKey(f.read())
    digest = sha256_bytes(path)
    sig = sk.sign(digest).signature
    payload = {"file": os.path.basename(path), "sha256_b64": base64.b64encode(digest).decode('ascii'),
               "sig_b64": base64.b64encode(sig).decode('ascii'), "meta": meta or {}}
    out = out_sig or (path + ".ed25519.sig.json")
    with open(out,"w",encoding="utf-8") as f: json.dump(payload,f,ensure_ascii=False,indent=2)
    print(f"[Ed25519] Signature générée : {out}")

def verify(path, vk_b64_path, sig_json):
    with open(vk_b64_path,"rb") as f: vk = VerifyKey(base64.b64decode(f.read()))
    with open(sig_json,"r",encoding="utf-8") as f: payload = json.load(f)
    
    digest = sha256_bytes(path)
    
    if base64.b64decode(payload["sha256_b64"]) != digest:
        print(f"{path}: {C.FAIL}FAIL: Le hash SHA-256 du fichier ne correspond pas!{C.END}"); return 3
    try:
        vk.verify(digest, base64.b64decode(payload["sig_b64"]))
        print(f"{path}: {C.OK}OK: Hash et Signature Ed25519 Valides.{C.END}"); return 0
    except BadSignatureError:
        print(f"{path}: {C.FAIL}FAIL: SIGNATURE CRYPTO INVALIDE!{C.END}"); return 4
    except Exception as e:
        print(f"[Ed25519 ERROR] Échec de la vérification : {e}", file=sys.stderr); return 5

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    p_gen = sub.add_parser("genkey"); p_gen.add_argument("--sk", default="ed25519_sk.bin"); p_gen.add_argument("--vk", default="ed25519_vk.b64")
    p1 = sub.add_parser("sign"); p1.add_argument("file"); p1.add_argument("--sk", required=True); p1.add_argument("--out"); p1.add_argument("--meta")
    p2 = sub.add_parser("verify"); p2.add_argument("file"); p2.add_argument("--vk", required=True); p2.add_argument("--sig", required=True)
    args = ap.parse_args()
    
    if args.cmd=="genkey": genkey(args.sk, args.vk)
    elif args.cmd=="sign": 
        meta_dict = None
        if args.meta:
            try: meta_dict = json.loads(args.meta)
            except json.JSONDecodeError: print(f"Métadonnées JSON invalides: {args.meta}", file=sys.stderr); sys.exit(1)
        sign(args.file, args.sk, args.out, meta_dict)
    elif args.cmd=="verify": sys.exit( verify(args.file, args.vk, args.sig) )
    else: ap.print_help()
