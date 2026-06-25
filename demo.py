from sign import sign_file
from verify import verify_file
from keygen import generate_keys

import csv
import os
import time


sign_results = []
verify_results = []


def main():
    input_file = "data_test/file_test_500mb.pdf"
    pk_ed = "key/ed25519_pub.key"
    sk_ed = "key/ed25519_priv.key"
    pk_falcon = "key/falcon_pub.key"
    sk_falcon = "key/falcon_priv.key"

    output_dir = "benchmark_outputs"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(100):
        signed_file = os.path.join(output_dir, f"test_signed_{i+1}.pdf")

        # Generate keys
        start_keygen = time.perf_counter()
        generate_keys(pk_ed, sk_ed, pk_falcon, sk_falcon)
        time_keygen = time.perf_counter() - start_keygen

        # Sign file
        (
            output_path,

            ed_parse_s,
            ed_hash_s,
            ed_crypto_s,
            ed_io_s,
            ed_total_s,

            fal_parse_s,
            fal_hash_s,
            fal_crypto_s,
            fal_io_s,
            fal_total_s
        ) = sign_file(
            input_file,
            signed_file,
            sk_ed,
            sk_falcon
        )

        # Verify file
        (
            ok,

            ed_parse_v,
            ed_hash_v,
            ed_crypto_v,
            ed_total_v,

            fal_parse_v,
            fal_hash_v,
            fal_crypto_v,
            fal_total_v,

            io_v,
            total_v
        ) = verify_file(
            output_path,
            pk_ed,
            pk_falcon
        )

        sign_results.append({
            "run": i + 1,
            "keygen_total": time_keygen,
            "ed_parse": ed_parse_s,
            "ed_hash": ed_hash_s,
            "ed_crypto": ed_crypto_s,
            "ed_io": ed_io_s,
            "ed_total": ed_total_s,
            "fal_parse": fal_parse_s,
            "fal_hash": fal_hash_s,
            "fal_crypto": fal_crypto_s,
            "fal_io": fal_io_s,
            "fal_total": fal_total_s,
        })

        verify_results.append({
            "run": i + 1,
            "ok": ok,
            "ed_parse": ed_parse_v,
            "ed_hash": ed_hash_v,
            "ed_crypto": ed_crypto_v,
            "ed_total": ed_total_v,
            "fal_parse": fal_parse_v,
            "fal_hash": fal_hash_v,
            "fal_crypto": fal_crypto_v,
            "fal_total": fal_total_v,
            "io": io_v,
            "total": total_v,
        })

        print(f"Run {i+1:03d} completed. Verify OK = {ok}")

    # Save sign results
    with open("bechmark/sign_benchmark_500mb.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sign_results[0].keys())
        writer.writeheader()
        writer.writerows(sign_results)

    # Save verify results
    with open("bechmark/verify_benchmark_500mb.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=verify_results[0].keys())
        writer.writeheader()
        writer.writerows(verify_results)

    print("Saved: sign_benchmark_500mb.csv")
    print("Saved: verify_benchmark_500mb.csv")


if __name__ == "__main__":
    main()