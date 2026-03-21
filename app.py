import streamlit as st
import os
import tempfile
from sign import sign_file
from verify import verify_file
from keygen import generate_keys

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="PQC Hybrid Signature",
    page_icon="logobig.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS CUSTOM LẤY CẢM HỨNG TỪ TAILWIND (app.tsx) ---
st.markdown("""
    <style>
    /* Màu nền tổng thể web giống bg-slate-50 */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Thiết kế Card giống file React */
    [data-testid="stVerticalBlock"] > div:has(div.stFrame) {
        background-color: #ffffff;
        border-radius: 0.75rem; /* rounded-xl */
        padding: 1.5rem; /* p-6 */
        border: 1px solid #e2e8f0; /* border-gray-200 */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); /* shadow-lg */
        margin-bottom: 1.5rem;
    }

    /* Style Header các phần */
    .section-header {
        font-size: 1.25rem; /* text-xl */
        font-weight: 600; /* font-semibold */
        color: #1e293b; /* text-slate-800 */
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 0.75rem;
    }

    /* Nút bấm Primary (Màu xanh Blue-600 giống Tailwind) */
    .stButton>button {
        background-color: #2563eb !important; 
        color: white !important;
        border-radius: 0.5rem !important; /* rounded-lg */
        height: 3rem !important;
        font-weight: 600 !important; /* font-semibold */
        border: none !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8 !important; /* hover:bg-blue-700 */
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.4);
    }

    /* Nút Download (Màu xám/đen) */
    .stDownloadButton>button {
        background-color: #f1f5f9 !important;
        color: #334155 !important;
        border: 1px solid #cbd5e1 !important;
    }
    .stDownloadButton>button:hover {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
    }

    /* Cảnh báo (Alerts) */
    div[data-testid="stAlert"] {
        border-radius: 0.5rem;
        border: none;
    }
    
    /* Upload file area */
    div[data-testid="stFileUploader"] {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8fafc;
        border: 1px dashed #cbd5e1;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (THANH ĐIỀU HƯỚNG) ---
with st.sidebar:
    # st.markdown("## PQC Hybrid System")
    st.markdown(
    "<h2 style='color:#1d4ed8; font-weight:700;'>PQC Hybrid System</h2>",
    unsafe_allow_html=True)
    st.caption("Bảo mật đa tầng Ed25519 + Falcon-512")
    st.markdown("---")
    # menu = st.radio(
    #     "ĐIỀU HƯỚNG CHỨC NĂNG",
    #     ["QUẢN LÝ KHÓA", "KÝ SỐ TÀI LIỆU", "XÁC THỰC TÀI LIỆU"],
    #     help="Chọn một tính năng để thao tác với hệ thống."
    # )
    if "menu" not in st.session_state:
        st.session_state.menu = "QUẢN LÝ KHÓA"

    st.markdown("### ĐIỀU HƯỚNG")

    if st.button("QUẢN LÝ KHÓA", use_container_width=True):
        st.session_state.menu = "QUẢN LÝ KHÓA"

    if st.button("KÝ SỐ TÀI LIỆU", use_container_width=True):
        st.session_state.menu = "KÝ SỐ TÀI LIỆU"

    if st.button("XÁC THỰC TÀI LIỆU", use_container_width=True):
        st.session_state.menu = "XÁC THỰC TÀI LIỆU"

    menu = st.session_state.menu
    st.markdown("---")
    st.info("Hệ thống đảm bảo an toàn dữ liệu tuyệt đối trước nguy cơ từ máy tính lượng tử.")

# --- 4. HẰNG SỐ & HÀM TRỢ GIÚP ---
PK_ED, SK_ED = "ed25519_pub.key", "ed25519_priv.key"
PK_FALCON, SK_FALCON = "falcon_pub.key", "falcon_priv.key"

def render_page_header(title, desc):
    st.markdown(f"<h1 style='color: #0f172a; font-size: 2.25rem; font-weight: 700; margin-bottom: 0.5rem;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;'>{desc}</p>", unsafe_allow_html=True)

# ==========================================
# TRANG 1: QUẢN LÝ KHÓA
# ==========================================

if os.path.exists(PK_ED):
    os.remove(PK_ED)
if os.path.exists(SK_ED):
    os.remove(SK_ED)
if os.path.exists(PK_FALCON):
    os.remove(PK_FALCON)
if os.path.exists(SK_FALCON):
    os.remove(SK_FALCON)

if menu == "QUẢN LÝ KHÓA":
    render_page_header("Khởi tạo bộ khóa Hybrid", "Tạo và lưu trữ các cặp khóa an toàn kết hợp thuật toán cổ điển và hậu lượng tử.")
    
    with st.container(border=True):
        st.markdown('<div class="section-header">Bảng điều khiển sinh khóa</div>', unsafe_allow_html=True)
        
        # Nút bấm đã được sửa lỗi logic (chỉ xóa/tạo khi bấm)
        if st.button("BẮT ĐẦU TẠO BỘ KHÓA MỚI", use_container_width=True):
            with st.spinner("Đang tính toán các tham số mạng tinh thể và đường cong elliptic..."):
                for k in [SK_ED, PK_ED, SK_FALCON, PK_FALCON]:
                    if os.path.exists(k): os.remove(k)
                generate_keys(PK_ED, SK_ED, PK_FALCON, SK_FALCON)
            st.success("Chúc mừng! Bộ khóa Hybrid đã được khởi tạo thành công.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hiển thị khu vực tải khóa nếu file đã tồn tại
    if os.path.exists(SK_ED) and os.path.exists(SK_FALCON):
        with st.container(border=True):
            st.markdown('<div class="section-header">Tải bộ khóa về máy</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Hệ mật mã Ed25519")
                with open(PK_ED, "rb") as f: st.download_button("Tải Public Key", f, PK_ED, use_container_width=True)
                with open(SK_ED, "rb") as f: st.download_button("Tải Private Key (Bảo mật)", f, SK_ED, use_container_width=True)
                
            with col2:
                st.markdown("#### Hệ mật mã Falcon-512")
                with open(PK_FALCON, "rb") as f: st.download_button("Tải Public Key", f, PK_FALCON, use_container_width=True)
                with open(SK_FALCON, "rb") as f: st.download_button("Tải Private Key (Bảo mật)", f, SK_FALCON, use_container_width=True)
    
    st.info("""
    **Hướng dẫn sử dụng**

    1. Nhấn **"BẮT ĐẦU TẠO BỘ KHÓA MỚI"** để hệ thống sinh khóa.
    2. Hệ thống sẽ tạo ra:
    - 2 khóa công khai (Public Key)
    - 2 khóa bí mật (Private Key)
    3. Sau khi tạo xong, tải các file khóa về máy.

    **Lưu ý quan trọng**
    - Không chia sẻ Private Key cho bất kỳ ai.
    - Nếu mất Private Key, bạn sẽ không thể ký tài liệu.
    - Public Key dùng để xác thực, có thể chia sẻ.
    """)

# ==========================================
# TRANG 2: KÝ SỐ
# ==========================================
elif menu == "KÝ SỐ TÀI LIỆU":
    render_page_header("Ký số tài liệu PDF", "Sử dụng khóa bí mật để đóng dấu điện tử lên tài liệu của bạn.")

    with st.container(border=True):
        st.markdown('<div class="section-header">1. Tải lên tài liệu cần ký</div>', unsafe_allow_html=True)
        pdf_file = st.file_uploader("Kéo thả file PDF vào đây", type=["pdf"], label_visibility="collapsed")
        
    if pdf_file:
        with st.container(border=True):
            st.markdown('<div class="section-header">2. Cung cấp khóa bí mật (Private Keys)</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            sk_ed = col1.file_uploader("Khóa Ed25519 Private (.key)", type=["key"])
            sk_fal = col2.file_uploader("Khóa Falcon Private (.key)", type=["key"])

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("THỰC HIỆN KÝ SỐ HYBRID", use_container_width=True):
                if sk_ed and sk_fal:
                    try:
                        with st.spinner("Đang xử lý chữ ký kép..."):
                            with tempfile.NamedTemporaryFile(delete=False) as p_tmp, \
                                 tempfile.NamedTemporaryFile(delete=False) as e_tmp, \
                                 tempfile.NamedTemporaryFile(delete=False) as f_tmp, \
                                 tempfile.NamedTemporaryFile(delete=False) as out_tmp:
                                
                                p_tmp.write(pdf_file.getvalue()); e_tmp.write(sk_ed.getvalue()); f_tmp.write(sk_fal.getvalue())
                                p_tmp.close(); e_tmp.close(); f_tmp.close()
                                
                                sign_file(p_tmp.name, out_tmp.name, e_tmp.name, f_tmp.name)
                                with open(out_tmp.name, "rb") as f: signed_bytes = f.read()
                            
                            for f_path in [p_tmp.name, e_tmp.name, f_tmp.name, out_tmp.name]:
                                if os.path.exists(f_path): os.remove(f_path)
                        
                        st.success("Tài liệu của bạn đã được ký an toàn!")
                        st.download_button("TẢI XUỐNG PDF ĐÃ KÝ", signed_bytes, file_name=f"signed_{pdf_file.name}", use_container_width=True)
                    except Exception as e:
                        st.error(f"Lỗi xử lý: {str(e)}")
                else:
                    st.warning("Vui lòng tải lên đầy đủ cả 2 file khóa bí mật.")
                    
    st.info("""
    **Hướng dẫn sử dụng**

    1. Tải lên file PDF cần ký.
    2. Tải lên 2 khóa bí mật:
    - Ed25519 Private Key
    - Falcon Private Key
    3. Nhấn **"THỰC HIỆN KÝ SỐ HYBRID"**.
    4. Tải xuống file PDF đã được ký.

    **Lưu ý**
    - File đầu vào phải là PDF.
    - Không chỉnh sửa file sau khi ký nếu không sẽ mất hiệu lực.
    - Có thể ký nhiều lần trên 1 file.
    """)

# ==========================================
# TRANG 3: XÁC THỰC
# ==========================================
else:
    render_page_header("Xác thực tính toàn vẹn", "Kiểm tra tài liệu đã ký có bị chỉnh sửa trái phép hay không.")

    with st.container(border=True):
        st.markdown('<div class="section-header">1. Tải lên tài liệu đã ký</div>', unsafe_allow_html=True)
        pdf_v = st.file_uploader("Kéo thả file PDF cần kiểm tra vào đây", type=["pdf"], label_visibility="collapsed")
        
    if pdf_v:
        with st.container(border=True):
            st.markdown('<div class="section-header">2. Cung cấp khóa công khai (Public Keys)</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            pk_ed = col1.file_uploader("Khóa Ed25519 Public (.key)", type=["key"])
            pk_fal = col2.file_uploader("Khóa Falcon Public (.key)", type=["key"])

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("TIẾN HÀNH XÁC THỰC", use_container_width=True):
                if pk_ed and pk_fal:
                    try:
                        with st.spinner("Đang đối soát chuỗi mã hóa đa tầng..."):
                            with tempfile.NamedTemporaryFile(delete=False) as p_tmp, \
                                 tempfile.NamedTemporaryFile(delete=False) as e_tmp, \
                                 tempfile.NamedTemporaryFile(delete=False) as f_tmp:
                                
                                p_tmp.write(pdf_v.getvalue()); e_tmp.write(pk_ed.getvalue()); f_tmp.write(pk_fal.getvalue())
                                p_tmp.close(); e_tmp.close(); f_tmp.close()
                                
                                is_valid = verify_file(p_tmp.name, e_tmp.name, f_tmp.name)
                            for f_path in [p_tmp.name, e_tmp.name, f_tmp.name]:
                                if os.path.exists(f_path): os.remove(f_path)
                        
                        if is_valid:
                            st.balloons()
                            st.success("### KẾT QUẢ: HỢP LỆ\nTài liệu nguyên bản và chữ ký khớp tuyệt đối. Không có dấu hiệu bị chỉnh sửa.")
                        else:
                            st.error("### KẾT QUẢ: KHÔNG HỢP LỆ\nCảnh báo: Tài liệu đã bị sửa đổi trái phép hoặc bộ khóa không khớp!")
                    except Exception as e:
                        st.error(f"Lỗi xác thực: Có thể định dạng file không đúng hoặc thiếu marker chữ ký. Chi tiết: {str(e)}")
                else:
                    st.warning("Vui lòng tải lên đầy đủ cả 2 file khóa công khai.")
    
    st.info("""
    **Hướng dẫn sử dụng**

    1. Tải lên file PDF đã ký.
    2. Tải lên 2 khóa công khai:
    - Ed25519 Public Key
    - Falcon Public Key
    3. Nhấn **"TIẾN HÀNH XÁC THỰC"**.

    **Lưu ý**
    - Phải dùng đúng Public Key tương ứng với Private Key đã ký.
    - Nếu file bị chỉnh sửa dù chỉ 1 ký tự → xác thực sẽ thất bại.
    """)