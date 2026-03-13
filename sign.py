from pqcrypto.sign import falcon_512
from nacl.signing import SigningKey
from utils import *

def sign_file(input_path: str, output_path: str, sk_ed: str, sk_falcon: str) -> str:
    #====================
    # sign ed25519
    #====================
    ed_prepare_file_with_placeholder(input_path, output_path)
    with open(output_path, "rb") as f:
        pdf_bytes = f.read()

    with open(sk_ed, "rb") as k:
        sk1 = k.read()

    byte_range, _, _ = ed_extract_byte_range_and_placeholder(pdf_bytes)
    digest = ed_compute_sha256_digest_for_byte_range(pdf_bytes, byte_range)
    sk = SigningKey(sk1)
    signature = signature = sk.sign(digest).signature

    signed_pdf_bytes = ed_embed_signature_into_pdf(pdf_bytes, signature)
    with open(output_path, "wb") as f:
        f.write(signed_pdf_bytes)

    #===================
    # sign falcon
    #===================

    falcon_prepare_file_with_placeholder(output_path, output_path)
    with open(output_path, "rb") as f:
        pdf_bytes = f.read()

    with open(sk_falcon, "rb") as k:
        sk2 = k.read()

    byte_range, _, _ = falcon_extract_byte_range_and_placeholder(pdf_bytes)
    digest = falcon_compute_shake256_digest_for_byte_range(pdf_bytes, byte_range)
    signature = falcon_512.sign(sk2, digest)

    signed_pdf_bytes = falcon_embed_signature_into_pdf(pdf_bytes, signature)
    with open(output_path, "wb") as f:
        f.write(signed_pdf_bytes)

    return output_path