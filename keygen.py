from pqcrypto.sign import falcon_512

def generate_keys(public_key: str , private_key: str):
    pk, sk = falcon_512.generate_keypair()

    with open(public_key, "wb") as f:
        f.write(pk)
    
    with open(private_key, "wb") as f:
        f.write(sk)

    print(len(pk))
    print(len(sk))