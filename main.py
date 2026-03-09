from sign import sign_file
from verify import verify_file
from keygen import generate_keys

def modify_pdf_middle_newfile(input_path: str, output_path: str):

    with open(input_path, "rb") as f:
        data = bytearray(f.read())

    mid = len(data) // 2

    data[mid:mid+5] = b"HACK!"

    with open(output_path, "wb") as f:
        f.write(data)

    return output_path

def main():

    input_file = "test.pdf"
    signed_file = "test_signed.pdf"
    modify_file = "test_modify.pdf"
    public_key = "falcon_priv.key"
    secret_key = "falcon_pub.key"

    print("=== TẠO KHÓA FALCON ===")
    generate_keys(public_key,secret_key)

    print("\n=== KÝ FILE PDF ===")
    sign_file(input_file, signed_file, secret_key)
    print("File đã ký:", signed_file)

    print("\n=== XÁC THỰC FILE SAU KHI KÝ ===")
    ok = verify_file(signed_file, public_key)
    print("Kết quả verify:", ok)

    print("\n=== CHỈNH SỬA FILE SAU KHI KÝ ===")
    modify_pdf_middle_newfile(signed_file, modify_file)

    print("File đã bị chỉnh sửa")

    print("\n=== XÁC THỰC LẠI ===")
    ok2 = verify_file(modify_file, public_key)
    print("Kết quả verify:", ok2)


if __name__ == "__main__":
    main()
