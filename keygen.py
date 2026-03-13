from pqcrypto.sign import falcon_512
from nacl.signing import SigningKey

def generate_keys(pk_ed: str , sk_ed: str, pk_falcon: str, sk_falcon: str):
    sk1 = SigningKey.generate()
    pk1 = sk1.verify_key

    sk_bytes = sk1.encode()
    pk_bytes = pk1.encode()

    with open(pk_ed, "wb") as f:
        f.write(pk_bytes)
    
    with open(sk_ed, "wb") as f:
        f.write(sk_bytes)

    print("do dai public key ed25519: ",len(pk_bytes))
    print("do dai purivate key ed25519: ",len(sk_bytes))

    pk2, sk2 = falcon_512.generate_keypair()

    with open(pk_falcon, "wb") as f:
        f.write(pk2)
    
    with open(sk_falcon, "wb") as f:
        f.write(sk2)

    print("do dai public key falcon: ",len(pk2))
    print("do dai public key falcon: ",len(sk2))