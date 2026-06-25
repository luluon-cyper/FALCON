from pqcrypto.sign import falcon_512
from nacl.signing import VerifyKey
from utils import *
import time


def verify_file(pdf_path: str, pk_ed: str, pk_falcon: str):
    
    with open(pk_ed, "rb") as f:
        pk1 = f.read()

    with open(pk_falcon, "rb") as f:
        pk2 = f.read()

    if len(pk1) != 32:
        return (False,
                0,0,0,0,
                0,0,0,0,
                0,0)

    if len(pk2) != 897:
        return (False,
                0,0,0,0,
                0,0,0,0,
                0,0)
    
    start_io = time.time()
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    time_io = time.time() - start_io

    
    index = -1
    ok_ed = False
    ok_falcon = False

    try:
        start_parse_ed = time.time()
        byte_range_ed, _, _ = extract_byte_range_and_placeholder(pdf_bytes, 0 ,index)
        sig_hex_ed = extract_signature_hex_from_pdf(pdf_bytes, 0 ,index)
        signature_ed = bytes.fromhex(sig_hex_ed.decode())
        time_parse_ed = time.time() - start_parse_ed

    except:
        time_parse_ed = 0
        ok_ed=False

    try:
        start_hash_ed = time.time()
        digest_ed = compute_sha512_digest_for_byte_range(pdf_bytes, byte_range_ed)
        time_hash_ed = time.time() - start_hash_ed

    except:
        time_hash_ed = 0
        ok_ed = False
    try:
        pk = VerifyKey(pk1)
        start_crypto_ed = time.time()

        pk.verify(digest_ed, signature_ed)
        time_crypto_ed = time.time() - start_crypto_ed
        ok_ed = True
    except:
        time_crypto_ed = 0
        ok_ed = False

    time_total_ed = (
        time_parse_ed +
        time_hash_ed +
        time_crypto_ed
    )

    try:
        start_parse_falcon = time.time()

        byte_range_falcon, _, _ = extract_byte_range_and_placeholder(
            pdf_bytes,
            1,
            index
        )

        sig_hex_falcon = extract_signature_hex_from_pdf(
            pdf_bytes,
            1,
            index
        )

        signature_falcon = bytes.fromhex(
            sig_hex_falcon.decode()
        )

        time_parse_falcon = (
            time.time() - start_parse_falcon
        )

    except Exception:
        time_parse_falcon = 0
        ok_falcon = False

    # Hash
    try:
        start_hash_falcon = time.time()

        digest_falcon = compute_shake256_digest_for_byte_range(
            pdf_bytes,
            byte_range_falcon
        )

        time_hash_falcon = (
            time.time() - start_hash_falcon
        )

    except Exception:
        time_hash_falcon = 0
        ok_falcon = False

    # Pure Crypto Verify
    try:
        start_crypto_falcon = time.time()

        ok_falcon = falcon_512.verify(
            pk2,
            digest_falcon,
            signature_falcon
        )

        time_crypto_falcon = (
            time.time() - start_crypto_falcon
        )

    except Exception:
        time_crypto_falcon = 0
        ok_falcon = False

    time_total_falcon = (
        time_parse_falcon +
        time_hash_falcon +
        time_crypto_falcon
    )

    time_total_verify = (
        time_io +
        time_total_ed +
        time_total_falcon
    )

    return (
        ok_ed and ok_falcon,

        # Ed25519
        time_parse_ed,
        time_hash_ed,
        time_crypto_ed,
        time_total_ed,

        # Falcon
        time_parse_falcon,
        time_hash_falcon,
        time_crypto_falcon,
        time_total_falcon,

        # Workflow
        time_io,
        time_total_verify
    )
    
