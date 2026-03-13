import hashlib 
import re 
from typing import Tuple, List

#==================================
# ED25519
#=================================
ED_SIG_MARKER_START = b"%%ED25519_PQ_SIG_START\n"
ED_SIG_MARKER_END = b"%%ED25519_PQ_SIG_END\n"

ED_BYTE_RANGE_TEMPLATE = b"ByteRange: [ %010d %010d %010d %010d ]\n"
ED_ZERO_BYTE_RANGE = ED_BYTE_RANGE_TEMPLATE % (0, 0, 0, 0)
ED_SIG_LEN=b"SigLength: %010d"
ED_SIG_LEN_SUFFIX = b"\n"
ED_SIG_LENGTH_REGEX = re.compile(rb"SigLength:\s*(\d{1,20})")
ED_CONTENTS_PREFIX = b"Contents: <"
ED_CONTENTS_SUFFIX = b">\n"

def ed_prepare_file_with_placeholder(input_path: str, output_path: str, placeholder_len: int = 128) -> None:
    with open(input_path, "rb") as f:
        original = f.read()
    
    hex_placeholder = b"0" * (placeholder_len*2)

    container = (
        ED_SIG_MARKER_START +
        ED_ZERO_BYTE_RANGE + 
        ED_SIG_LEN % placeholder_len +
        ED_SIG_LEN_SUFFIX +
        ED_CONTENTS_PREFIX +
        hex_placeholder +
        ED_CONTENTS_SUFFIX +
        ED_SIG_MARKER_END
    )

    combined = original + container

    start1 = 0
    len1 = combined.rfind(ED_SIG_LEN[:10])
    start2 = combined.find(ED_CONTENTS_PREFIX, len1) + len(ED_CONTENTS_PREFIX) + placeholder_len*2 + len(ED_CONTENTS_SUFFIX)
    len2 = len(combined) - start2

    byte_range = ED_BYTE_RANGE_TEMPLATE % (start1, len1, start2, len2)

    patched = combined.replace(ED_ZERO_BYTE_RANGE, byte_range, 1)

    with open(output_path, "wb") as f:
        f.write(patched)

def ed_extract_byte_range_and_placeholder(pdf_bytes: bytes, index: int = -1) -> Tuple[List[int], int, int]:
    containers = []

    pos = 0
    while True:
        start = pdf_bytes.find(ED_SIG_MARKER_START, pos)
        if start == -1:
            break
        
        end = pdf_bytes.find(ED_SIG_MARKER_END, start)
        if end == -1:
            raise RuntimeError("Container chữ ký bị lỗi")
        
        containers.append((start, end))
        pos = end + len(ED_SIG_MARKER_END)
        
    if not containers:
        raise RuntimeError("Không tìm thấy chữ ký")
    
    if index < 0:
        index = len(containers) + index

    if index >= len(containers):
        raise RuntimeError("Index chữ ký không hợp lệ")
    
    marker_start, marker_end = containers[index]

    template = re.search(rb"ByteRange:\s*\[\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\]", pdf_bytes[marker_start:marker_end])

    byte_range = [
        int(template.group(1)),
        int(template.group(2)),
        int(template.group(3)),
        int(template.group(4)),
    ]

    return byte_range, marker_start, marker_end+len(ED_SIG_MARKER_END)

def ed_compute_sha256_digest_for_byte_range(pdf_bytes: bytes, byte_range: List[int]) -> bytes:
    offset1, length1, offset2, length2 = byte_range
    
    part1 = pdf_bytes[offset1: offset1 + length1]
    part2 = pdf_bytes[offset2: offset2 + length2]

    message = part1+part2
    return message


def ed_embed_signature_into_pdf(pdf_bytes: bytes, signature: bytes, index: int = -1) -> bytes:
    _, maker_start, maker_end = ed_extract_byte_range_and_placeholder(pdf_bytes, index)
    
    contents_start = pdf_bytes.find(ED_CONTENTS_PREFIX, maker_start, maker_end)
    contents_end = pdf_bytes.find(ED_CONTENTS_SUFFIX, contents_start, maker_end)

    hex_len= contents_end-(contents_start + len(ED_CONTENTS_PREFIX))

    sig_hex = signature.hex().encode()

    padded_sig = sig_hex + b"0" * (hex_len - len(sig_hex))

    pdf_bytes = (
        pdf_bytes[:contents_start+len(ED_CONTENTS_PREFIX)] +
        padded_sig +
        pdf_bytes[contents_end:]
    )

    sig_len_str = ED_SIG_LEN % len(sig_hex)

    template = ED_SIG_LENGTH_REGEX.search(pdf_bytes, maker_start, maker_end)
    if template:
        start = template.start()
        end = template.end()

        pdf_bytes = (
            pdf_bytes[:start] +
            sig_len_str +
            pdf_bytes[end:]
        )
    
    return pdf_bytes

def ed_extract_signature_hex_from_pdf(pdf_bytes: bytes, index: int = -1) -> bytes:
    _, marker_start, marker_end = ed_extract_byte_range_and_placeholder(pdf_bytes , index)

    m = ED_SIG_LENGTH_REGEX.search(pdf_bytes, marker_start, marker_end)

    sig_len = int(m.group(1))

    sign_start = pdf_bytes.find(ED_CONTENTS_PREFIX,marker_start) + len(ED_CONTENTS_PREFIX)

    sign_byte = pdf_bytes[sign_start:sign_start+sig_len]

    return sign_byte


#=======================
# FALCON
#=======================

SIG_MARKER_START = b"%%FALCON_PQ_SIG_START\n"
SIG_MARKER_END = b"%%FALCON_PQ_SIG_END\n"

BYTE_RANGE_TEMPLATE = b"ByteRange: [ %010d %010d %010d %010d ]\n"
ZERO_BYTE_RANGE = BYTE_RANGE_TEMPLATE % (0, 0, 0, 0)
SIG_LEN=b"SigLength: %010d"
SIG_LEN_SUFFIX = b"\n"
SIG_LENGTH_REGEX = re.compile(rb"SigLength:\s*(\d{1,20})")
CONTENTS_PREFIX = b"Contents: <"
CONTENTS_SUFFIX = b">\n"

def falcon_prepare_file_with_placeholder(input_path: str, placeholder_len: int = 2048) -> None:
    with open(input_path, "rb") as f:
        original = f.read()
    
    hex_placeholder = b"0" * (placeholder_len*2)

    container = (
        SIG_MARKER_START +
        ZERO_BYTE_RANGE + 
        SIG_LEN % placeholder_len +
        SIG_LEN_SUFFIX +
        CONTENTS_PREFIX +
        hex_placeholder +
        CONTENTS_SUFFIX +
        SIG_MARKER_END
    )

    combined = original + container

    start1 = 0
    len1 = combined.rfind(SIG_LEN[:10])
    start2 = combined.find(CONTENTS_PREFIX, len1) + len(CONTENTS_PREFIX) + placeholder_len*2 + len(CONTENTS_SUFFIX)
    len2 = len(combined) - start2

    byte_range = BYTE_RANGE_TEMPLATE % (start1, len1, start2, len2)

    patched = combined.replace(ZERO_BYTE_RANGE, byte_range, 1)

    with open(input_path, "wb") as f:
        f.write(patched)

def falcon_extract_byte_range_and_placeholder(pdf_bytes: bytes, index: int = -1) -> Tuple[List[int], int, int]:
    containers = []

    pos = 0
    while True:
        start = pdf_bytes.find(SIG_MARKER_START, pos)
        if start == -1:
            break
        
        end = pdf_bytes.find(SIG_MARKER_END, start)
        if end == -1:
            raise RuntimeError("Container chữ ký bị lỗi")
        
        containers.append((start, end))
        pos = end + len(SIG_MARKER_END)
        
    if not containers:
        raise RuntimeError("Không tìm thấy chữ ký")
    
    if index < 0:
        index = len(containers) + index

    if index >= len(containers):
        raise RuntimeError("Index chữ ký không hợp lệ")
    
    marker_start, marker_end = containers[index]

    template = re.search(rb"ByteRange:\s*\[\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\]", pdf_bytes[marker_start:marker_end])

    byte_range = [
        int(template.group(1)),
        int(template.group(2)),
        int(template.group(3)),
        int(template.group(4)),
    ]

    return byte_range, marker_start, marker_end+len(SIG_MARKER_END)


def falcon_compute_shake256_digest_for_byte_range(pdf_bytes: bytes, byte_range: List[int], digest_len = 64) -> bytes:
    offset1, length1, offset2, length2 = byte_range
    
    part1 = pdf_bytes[offset1: offset1 + length1]
    part2 = pdf_bytes[offset2: offset2 + length2]

    message = part1+part2
    shake = hashlib.shake_256(message)
    return shake.digest(digest_len)


def falcon_embed_signature_into_pdf(pdf_bytes: bytes, signature: bytes, index: int = -1) -> bytes:
    _, maker_start, maker_end = falcon_extract_byte_range_and_placeholder(pdf_bytes, index)
    
    contents_start = pdf_bytes.find(CONTENTS_PREFIX, maker_start, maker_end)
    contents_end = pdf_bytes.find(CONTENTS_SUFFIX, contents_start, maker_end)

    hex_len= contents_end-(contents_start + len(CONTENTS_PREFIX))

    sig_hex = signature.hex().encode()

    padded_sig = sig_hex + b"0" * (hex_len - len(sig_hex))

    pdf_bytes = (
        pdf_bytes[:contents_start+len(CONTENTS_PREFIX)] +
        padded_sig +
        pdf_bytes[contents_end:]
    )

    sig_len_str = SIG_LEN % len(sig_hex)

    template = SIG_LENGTH_REGEX.search(pdf_bytes, maker_start, maker_end)
    if template:
        start = template.start()
        end = template.end()

        pdf_bytes = (
            pdf_bytes[:start] +
            sig_len_str +
            pdf_bytes[end:]
        )
    
    return pdf_bytes

def falcon_extract_signature_hex_from_pdf(pdf_bytes: bytes, index: int = -1) -> bytes:
    _, marker_start, marker_end = falcon_extract_byte_range_and_placeholder(pdf_bytes , index)

    m = SIG_LENGTH_REGEX.search(pdf_bytes, marker_start, marker_end)

    sig_len = int(m.group(1))

    sign_start = pdf_bytes.find(CONTENTS_PREFIX,marker_start) + len(CONTENTS_PREFIX)

    sign_byte = pdf_bytes[sign_start:sign_start+sig_len]

    return sign_byte


