# eSign v1.0 - Hệ thống Ký số Hybrid (Ed25519 & Falcon-512)

<p align="center">
  <img src="assets/logobig.jpg" alt="eSign Logo" width="150"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/YOUR_GITHUB_USERNAME/esign-pqc-hybrid?style=flat-square&color=blue" alt="Current Release"/>
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey?style=flat-square&logo=windows" alt="Platform"/>
  <img src="https://img.shields.io/badge/Algorithms-Ed25519%20%2B%20Falcon--512-orange?style=flat-square" alt="Cryptography Algorithms"/>
  <img src="https://img.shields.io/github/license/YOUR_GITHUB_USERNAME/esign-pqc-hybrid?style=flat-square" alt="License"/>
</p>

---

## Giới thiệu

**eSign v1.0** là một ứng dụng phần mềm Desktop tiên phong trong lĩnh vực mật mã, kết hợp sức mạnh của ký số truyền thống với các chuẩn mật mã hậu lượng tử (Post-Quantum Cryptography - PQC). 

Ứng dụng cung cấp giải pháp ký số **đa tầng (hybrid)** đảm bảo tính toàn vẹn và xác thực của tài liệu, chống lại nguy cơ bị bẻ khóa bởi máy tính lượng tử trong tương lai. Giao diện trực quan giúp bất kỳ ai cũng có thể tạo khóa, ký tài liệu và xác thực một cách dễ dàng.

## Tính năng nổi bật

* **Khởi Tạo Khóa Hybrid**: Sinh ngẫu nhiên bộ khóa (Public/Private) kết hợp giữa chuẩn cổ điển **Ed25519** và chuẩn hậu lượng tử mạng tinh thể **Falcon-512**.
* **Ký Số Đa Tầng**: Ký tài liệu PDF bằng cách sử dụng khóa bí mật của cả hai thuật toán, tạo ra một lớp bảo vệ kép.
* **Xác Thực Toàn Vẹn**: Kiểm tra đồng thời cả hai thành phần của chữ ký để đảm bảo tài liệu không bị chỉnh sửa trái phép.
* **Giao diện Desktop Độc Lập**: Hoạt động mượt mà như một phần mềm bình thường mà không cần cấu hình môi trường phức tạp.

## Tải về và Cài đặt

1. Chuyển đến trang **[Releases](https://github.com/YOUR_GITHUB_USERNAME/esign-pqc-hybrid/releases/latest)** của dự án.
2. Tải xuống file cài đặt **`eSign_v1.0_Setup.exe`**.
3. Chạy file vừa tải về và bấm **Next** để cài đặt.
4. Mở ứng dụng **eSign** từ shortcut trên màn hình Desktop của bạn và sử dụng.

### Yêu cầu hệ thống
* Python 3.9+
* Hệ điều hành Windows