from pqcrypto.sign import falcon_512
from nacl.signing import VerifyKey
from utils import *

def verify_file(pdf_path: str, pk_ed: str, pk_falcon: str) -> bool:
    
    with open(pk_ed, "rb") as f:
        pk1 = f.read()

    with open(pk_falcon, "rb") as f:
        pk2 = f.read()

    if len(pk1) != 32:
        return False

    if len(pk2) != 897:
        return False
    
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    
    index = -1
    ok_ed = False
    ok_falcon = False
    try:
        byte_range_ed, _, _ = extract_byte_range_and_placeholder(pdf_bytes, 0 ,index)
    except:
        return False
    digest_ed = compute_sha512_digest_for_byte_range(pdf_bytes, byte_range_ed)
    sig_hex_ed = extract_signature_hex_from_pdf(pdf_bytes, 0 ,index)
    signature_ed = bytes.fromhex(sig_hex_ed.decode())

    try:
        pk = VerifyKey(pk1)
        pk.verify(digest_ed, signature_ed)
        ok_ed = True
    except:
        ok_ed = False
    try:
        byte_range_falcon, _, _ =extract_byte_range_and_placeholder(pdf_bytes, 1 , index)
    except:
        return False
    digest_falcon = compute_shake256_digest_for_byte_range(pdf_bytes , byte_range_falcon)
    sig_hex_falcon=extract_signature_hex_from_pdf(pdf_bytes, 1, index)
    signature_falcon = bytes.fromhex(sig_hex_falcon.decode())
    ok_falcon = falcon_512.verify(pk2, digest_falcon, signature_falcon)

    if(ok_ed and ok_falcon):
        return True
    else:
        return  False
        
