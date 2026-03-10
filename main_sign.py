import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from sign import sign_file

pdf_input = ""
key_input = ""
output_file = "signed.pdf"

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

def process_pdf(pdf_input, output_file, key_input):
    sign_file(pdf_input, output_file, key_input)

def run_process():
    if not pdf_input or not key_input:
        messagebox.showwarning("Lỗi", "Vui lòng chọn đầy đủ file PDF và Key!")
        return

    progress['value'] = 0
    root.update_idletasks()

    process_pdf(pdf_input, output_file, key_input)

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

root = tk.Tk()
root.title("FALCON")
root.geometry("520x420")
root.configure(bg="#f0f2f5")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

lbl_title = ttk.Label(root, text="HỆ THỐNG KÝ FALCON", style="Header.TLabel", background="#f0f2f5")
lbl_title.pack(pady=20)

frame_input = ttk.LabelFrame(root, text=" file ký (pdf) và khóa riêng (private key) ", padding=15)
frame_input.pack(padx=20, fill="x")

ttk.Button(frame_input, text="Chọn PDF", width=12, command=choose_pdf).grid(row=0, column=0, pady=5, sticky="w")
lbl_pdf_name = ttk.Label(frame_input, text="Chưa có tệp nào được chọn", font=("Segoe UI", 9, "italic"))
lbl_pdf_name.grid(row=0, column=1, padx=10, sticky="w")

ttk.Button(frame_input, text="Chọn KEY", width=12, command=choose_key).grid(row=1, column=0, pady=5, sticky="w")
lbl_key_name = ttk.Label(frame_input, text="Chưa có khóa nào được chọn", font=("Segoe UI", 9, "italic"))
lbl_key_name.grid(row=1, column=1, padx=10, sticky="w")

frame_action = ttk.Frame(root, padding=10)
frame_action.pack(fill="x", padx=20)

btn_execute = ttk.Button(frame_action, text="BẮT ĐẦU KÝ", command=run_process)
btn_execute.pack(pady=10, fill="x")

progress = ttk.Progressbar(frame_action, orient="horizontal", length=100, mode="determinate")
progress.pack(fill="x", pady=5)

frame_output = ttk.LabelFrame(root, text=" file đã ký ", padding=15)
frame_output.pack(padx=20, pady=10, fill="x")

lbl_status = ttk.Label(frame_output, text="Sẵn sàng xử lý...", font=("Segoe UI", 10, "bold"))
lbl_status.grid(row=0, column=0, sticky="w")

btn_download = ttk.Button(frame_output, text="Tải xuống (.pdf)", state="disabled", command=download_file)
btn_download.grid(row=0, column=1, padx=20, sticky="e")

ttk.Label(root, text="Phiên bản 1.0.0", font=("Segoe UI", 8), foreground="#95a5a6").pack(side="bottom", pady=5)

root.mainloop()