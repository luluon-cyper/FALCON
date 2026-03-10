from pqcrypto.sign import falcon_512
from utils import *

def sign_file(input_path: str, output_path: str, secret_key: str) -> str:
    prepare_file_with_placeholder(input_path, output_path)
    with open(output_path, "rb") as f:
        pdf_bytes = f.read()

    with open(secret_key, "rb") as k:
        private_key = k.read()

    byte_range, _, _ = extract_byte_range_and_placeholder(pdf_bytes)
    digest = compute_shake256_digest_for_byte_range(pdf_bytes, byte_range)
    signature = falcon_512.sign(private_key, digest)

    signed_pdf_bytes = embed_signature_into_pdf(pdf_bytes, signature)
    with open(output_path, "wb") as f:
        f.write(signed_pdf_bytes)

    return output_path