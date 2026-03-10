import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil

# --- Biến toàn cục ---
pdf_input = ""
key_input = ""
output_file = "output.pdf"

# --- Hàm xử lý ---
def choose_pdf():
    global pdf_input
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if path:
        pdf_input = path
        lbl_pdf_name.config(text=os.path.basename(path), foreground="#2ecc71")

def choose_key():
    global key_input
    path = filedialog.askopenfilename(filetypes=[("KEY files", "*.key")])
    if path:
        key_input = path
        lbl_key_name.config(text=os.path.basename(path), foreground="#2ecc71")

def process_pdf(input_pdf, key_file, output_pdf):
    # Giả lập xử lý
    with open(output_pdf, "wb") as f:
        f.write(b"%PDF-1.4\n%demo output\n")

def run_process():
    if not pdf_input or not key_input:
        messagebox.showwarning("Lỗi", "Vui lòng chọn đầy đủ file PDF và Key!")
        return

    # Hiệu ứng Progress Bar giả lập
    progress['value'] = 0
    root.update_idletasks()
    process_pdf(pdf_input, key_input, output_file)
    progress['value'] = 100
    
    lbl_status.config(text="Xử lý hoàn tất!", foreground="#27ae60")
    btn_download.config(state="normal")

def download_file():
    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )
    if save_path:
        shutil.copy(output_file, save_path)
        messagebox.showinfo("Thành công", "Đã lưu file thành công!")

# ================= GIAO DIỆN (GUI) =================

root = tk.Tk()
root.title("Công cụ xử lý PDF chuyên nghiệp")
root.geometry("520x420")
root.configure(bg="#f0f2f5")

# Style cho giao diện hiện đại
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

# 1. TIÊU ĐỀ
lbl_title = ttk.Label(root, text="HỆ THỐNG XỬ LÝ & MÃ HÓA PDF", style="Header.TLabel", background="#f0f2f5")
lbl_title.pack(pady=20)

# 2. KHUNG CHỌN FILE (INPUT)
frame_input = ttk.LabelFrame(root, text=" Cấu hình đầu vào ", padding=15)
frame_input.pack(padx=20, fill="x")

# Grid cho Input
# Hàng 1: PDF
ttk.Button(frame_input, text="Chọn PDF", width=12, command=choose_pdf).grid(row=0, column=0, pady=5, sticky="w")
lbl_pdf_name = ttk.Label(frame_input, text="Chưa có tệp nào được chọn", font=("Segoe UI", 9, "italic"))
lbl_pdf_name.grid(row=0, column=1, padx=10, sticky="w")

# Hàng 2: KEY
ttk.Button(frame_input, text="Chọn KEY", width=12, command=choose_key).grid(row=1, column=0, pady=5, sticky="w")
lbl_key_name = ttk.Label(frame_input, text="Chưa có khóa nào được chọn", font=("Segoe UI", 9, "italic"))
lbl_key_name.grid(row=1, column=1, padx=10, sticky="w")

# 3. KHUNG THỰC THI (ACTION)
frame_action = ttk.Frame(root, padding=10)
frame_action.pack(fill="x", padx=20)

btn_execute = ttk.Button(frame_action, text="BẮT ĐẦU XỬ LÝ", command=run_process)
btn_execute.pack(pady=10, fill="x")

progress = ttk.Progressbar(frame_action, orient="horizontal", length=100, mode="determinate")
progress.pack(fill="x", pady=5)

# 4. KHUNG KẾT QUẢ (OUTPUT)
frame_output = ttk.LabelFrame(root, text=" Kết quả đầu ra ", padding=15)
frame_output.pack(padx=20, pady=10, fill="x")

lbl_status = ttk.Label(frame_output, text="Sẵn sàng xử lý...", font=("Segoe UI", 10, "bold"))
lbl_status.grid(row=0, column=0, sticky="w")

btn_download = ttk.Button(frame_output, text="Tải xuống (.pdf)", state="disabled", command=download_file)
btn_download.grid(row=0, column=1, padx=20, sticky="e")

# Footer
ttk.Label(root, text="Phiên bản 1.0.0", font=("Segoe UI", 8), foreground="#95a5a6").pack(side="bottom", pady=5)

root.mainloop()