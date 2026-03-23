from pqcrypto.sign import falcon_512
from nacl.signing import SigningKey
import time

def generate_keys(pk_ed: str , sk_ed: str, pk_falcon: str, sk_falcon: str):
    start_genkey_ed25519=time.time()
    sk1 = SigningKey.generate()
    pk1 = sk1.verify_key

    sk_bytes = sk1.encode()
    pk_bytes = pk1.encode()

    with open(pk_ed, "wb") as f:
        f.write(pk_bytes)
    
    with open(sk_ed, "wb") as f:
        f.write(sk_bytes)
    print("thời gian sinh khóa ed25519: ",time.time()-start_genkey_ed25519)

    start_genkey_falcon=time.time()
    pk2, sk2 = falcon_512.generate_keypair()


    with open(pk_falcon, "wb") as f:
        f.write(pk2)
    
    with open(sk_falcon, "wb") as f:
        f.write(sk2)
    print("thời gian sinh khóa falcon: ",time.time()-start_genkey_falcon)
