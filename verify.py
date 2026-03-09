from pqcrypto.sign import falcon_512
from utils import *


def verify_file(pdf_path: str, public_key: str) -> bool:
    
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    with open(public_key, "rb") as f:
        pk = f.read()
    
    index = 0
    while True:
        try:
            byte_range, _, _ = extract_byte_range_and_placeholder(pdf_bytes, index)
        except:
            return False
        digest = compute_shake256_digest_for_byte_range(pdf_bytes, byte_range)
        sig_hex = extract_signature_hex_from_pdf(pdf_bytes, index)
        signature = bytes.fromhex(sig_hex.decode())

        ok = falcon_512.verify(pk, digest, signature)
        if ok:
            return True
        index+=1


