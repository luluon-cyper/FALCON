import streamlit as st
import os
import tempfile
from sign import sign_file
from verify import verify_file
from keygen import generate_keys

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="PQC Digital Signature",
    page_icon="🔐",
    layout="wide"
)

# --- 2. GIAO DIỆN CSS ĐỒNG NHẤT ---
st.markdown("""
    <style>
    /* Bo góc và đổ bóng cho các vùng nội dung */
    [data-testid="stVerticalBlock"] > div:has(div.stFrame) {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #ececf1;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    /* Style cho các header chuyên dụng */
    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    /* Làm đẹp các nút bấm */
    .stButton>button {
        border-radius: 10px;
        height: 3.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (THANH ĐIỀU HƯỚNG) ---
with st.sidebar:
    st.title("PQC Hybrid System")
    st.markdown("---")
    menu = st.radio(
        "LUỒNG CÔNG VIỆC:",
        ["🔑 KHỞI TẠO KHÓA", "✍️ KÝ TÀI LIỆU", "✅ XÁC THỰC SỐ"],
        help="Thực hiện theo thứ tự từ trên xuống dưới nếu bạn là người dùng mới."
    )
    st.markdown("---")
    st.caption("Công nghệ: **Hybrid Ed25519 + Falcon-512**")
    st.info("Hệ thống bảo mật đa tầng, an toàn trước máy tính lượng tử.")

# --- 4. CÁC HÀM TRỢ GIÚP (HELPER FUNCTIONS) ---
def render_header(title, subtitle, icon):
    st.markdown(f"## {icon} {title}")
    st.markdown(f"<p style='color: #6b7280; font-size: 1.1rem;'>{subtitle}</p>", unsafe_allow_html=True)
    st.divider()

PK_ED, SK_ED = "ed25519_pub.key", "ed25519_priv.key"
PK_FALCON, SK_FALCON = "falcon_pub.key", "falcon_priv.key"

# ==========================================
# TRANG 1: QUẢN LÝ KHÓA
# ==========================================


if menu == "🔑 KHỞI TẠO KHÓA":
    if os.path.exists(SK_ED):
        os.remove(SK_ED)
    if os.path.exists(PK_ED):
        os.remove(PK_ED)
    if os.path.exists(SK_FALCON):
        os.remove(SK_FALCON)
    if os.path.exists(PK_FALCON):
        os.remove(PK_FALCON)

    render_header("Quản lý Khóa Mã hóa", "Tạo và lưu trữ các cặp khóa Hybrid (Cổ điển & Hậu lượng tử)", "🔑")
    
    col_info, col_main = st.columns([1, 2], gap="large")
    
    with col_info:
        st.info("💡 **Lưu ý quan trọng:**\n\n1. **Private Key:** Tuyệt đối giữ bí mật.\n2. **Public Key:** Dùng để gửi cho người nhận xác thực.\n3. Khóa cũ sẽ bị ghi đè nếu bạn tạo khóa mới.")

    with col_main:
        with st.container(border=True):
            st.markdown('<div class="section-header">🛠️ Công cụ sinh khóa</div>', unsafe_allow_html=True)
            if st.button("🔄 BẮT ĐẦU TẠO BỘ KHÓA MỚI", type="primary", use_container_width=True):
                with st.spinner("Đang tính toán các tham số an toàn..."):
                    generate_keys(PK_ED, SK_ED, PK_FALCON, SK_FALCON)
                st.success("Chúc mừng! Bộ khóa Hybrid đã được khởi tạo thành công.")

            st.markdown("---")
            st.markdown('<div class="section-header">📥 Tải bộ khóa về máy</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Nhóm Ed25519**")
                for label, path in [("Public Key", PK_ED), ("Private Key", SK_ED)]:
                    if os.path.exists(path):
                        with open(path, "rb") as f:
                            st.download_button(f"Tải {label}", f, file_name=path, key=f"dl_{path}")
            with c2:
                st.write("**Nhóm FALCON**")
                for label, path in [("Public Key", PK_FALCON), ("Private Key", SK_FALCON)]:
                    if os.path.exists(path):
                        with open(path, "rb") as f:
                            st.download_button(f"Tải {label}", f, file_name=path, key=f"dl_{path}")


# ==========================================
# TRANG 2: KÝ SỐ
# ==========================================
elif menu == "✍️ KÝ TÀI LIỆU":
    render_header("Ký số Tài liệu PDF", "Sử dụng khóa bí mật để tạo chữ ký Hybrid vào tệp tin", "✍️")

    col_guide, col_main = st.columns([1, 2], gap="large")
    
    with col_guide:
        st.warning("📋 **Quy trình ký:**\n\n1. Chọn tệp PDF gốc.\n2. Tải lên 2 file khóa Private tương ứng.\n3. Hệ thống sẽ tạo file mới có đuôi `signed.pdf`.")

    with col_main:
        with st.container(border=True):
            st.markdown('<div class="section-header">📄 1. Chọn tệp tin nguồn</div>', unsafe_allow_html=True)
            pdf_file = st.file_uploader("Kéo thả file PDF vào đây", type=["pdf"], label_visibility="collapsed")
            
            st.markdown('<div class="section-header">🔑 2. Cung cấp khóa bí mật</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            sk_ed = c1.file_uploader("Ed25519 Private (.key)", type=["key"])
            sk_fal = c2.file_uploader("Falcon Private (.key)", type=["key"])

            if st.button("🚀 THỰC HIỆN KÝ SỐ", type="primary", use_container_width=True):
                if pdf_file and sk_ed and sk_fal:
                    try:
                        with st.status("Đang thực hiện ký số kép...", expanded=False) as status:
                            with tempfile.NamedTemporaryFile(delete=False) as p_tmp, \
                                 tempfile.NamedTemporaryFile(delete=False) as e_tmp, \
                                 tempfile.NamedTemporaryFile(delete=False) as f_tmp, \
                                 tempfile.NamedTemporaryFile(delete=False) as out_tmp:
                                
                                p_tmp.write(pdf_file.getvalue()); e_tmp.write(sk_ed.getvalue()); f_tmp.write(sk_fal.getvalue())
                                p_tmp.close(); e_tmp.close(); f_tmp.close()
                                
                                sign_file(p_tmp.name, out_tmp.name, e_tmp.name, f_tmp.name)
                                
                                with open(out_tmp.name, "rb") as f: 
                                    signed_bytes = f.read()
                            
                            for f_path in [p_tmp.name, e_tmp.name, f_tmp.name, out_tmp.name]:
                                if os.path.exists(f_path): os.remove(f_path)
                            
                            status.update(label="Ký số hoàn tất!", state="complete")
                        
                        st.success("Tài liệu của bạn đã được ký an toàn.")
                        st.download_button("⬇️ TẢI PDF ĐÃ KÝ", signed_bytes, file_name=f"signed_{pdf_file.name}", use_container_width=True)
                    
                    except ValueError as e:
                        st.error(f"❌ **Lỗi xác thực khóa:** {str(e)}")
                    except Exception as e:
                        st.error(f"⚠️ **Lỗi hệ thống:** {str(e)}")
                else:
                    st.error("Vui lòng tải lên đầy đủ các tệp yêu cầu.")

# ==========================================
# TRANG 3: XÁC THỰC
# ==========================================
else:
    render_header("Xác thực Tính toàn vẹn", "Kiểm tra xem tài liệu có bị chỉnh sửa hay không", "✅")
    col_guide, col_main = st.columns([1, 2], gap="large")

    with col_guide:
        st.info("🧐 **Cách kiểm tra:**\n\nChữ ký chỉ hợp lệ khi bạn sử dụng đúng **Khóa công khai** và tệp PDF không bị thay đổi.")

    with col_main:
        with st.container(border=True):
            st.markdown('<div class="section-header">📄 1. Chọn tệp PDF đã ký</div>', unsafe_allow_html=True)
            pdf_v = st.file_uploader("Tải lên PDF cần xác thực", type=["pdf"], label_visibility="collapsed")
            
            st.markdown('<div class="section-header">🔑 2. Cung cấp khóa công khai</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            pk_ed = c1.file_uploader("Ed25519 Public (.key)", type=["key"])
            pk_fal = c2.file_uploader("Falcon Public (.key)", type=["key"])

            if st.button("🔍 KIỂM TRA TÍNH HỢP LỆ", type="primary", use_container_width=True):
                if pdf_v and pk_ed and pk_fal:
                    try:
                        with st.spinner("Đang đối soát chữ ký lượng tử..."):
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
                            st.success("### ✅ KẾT QUẢ: HỢP LỆ\nTài liệu nguyên bản và chữ ký khớp tuyệt đối.")
                        else:
                            st.error("### ❌ KẾT QUẢ: KHÔNG HỢP LỆ\nCảnh báo: Tài liệu đã bị sửa đổi hoặc khóa không khớp.")
                    
                    except ValueError as e:
                        st.error(f"❌ **Khóa không đúng định dạng:** {str(e)}")
                    except Exception as e:
                        st.error(f"⚠️ **Xảy ra lỗi trong quá trình xác thực:** {str(e)}")
                else:
                    st.error("Thiếu thông tin đầu vào.")