# 🤖 Macro Tool Pro Max (Auto Click & Keyboard)(Vibe)

**Macro Tool Pro Max** là công cụ hỗ trợ ghi và phát lại các thao tác chuột (trái, phải, giữa, cuộn) và bàn phím (bao gồm cả tổ hợp phím phức tạp). Phần mềm giúp bạn tự động hóa các công việc lặp đi lặp lại một cách chính xác và hiệu quả.

---

## ✨ Tính năng nổi bật
- **Ghi hình đa năng:** Lưu lại di chuyển chuột, click chuột (Trái/Phải/Giữa), cuộn chuột và nhấn phím.
- **Hỗ trợ tổ hợp phím:** Xử lý mượt mà các tổ hợp như `Ctrl+C`, `Ctrl+V`, `Alt+Tab`, `Ctrl+T`, `Shift+A`...
- **Vòng lặp thông minh:** Tùy chỉnh số lần lặp lại và hiển thị tiến trình vòng lặp thực tế trên giao diện.
- **Luôn hiển thị trên cùng:** Giao diện nhỏ gọn, luôn nổi trên các cửa sổ khác để dễ điều khiển.
- **Ngắt khẩn cấp (Fail-Safe):** Di chuyển chuột thật mạnh vào 4 góc màn hình để dừng ngay lập tức nếu macro chạy sai.

---

## ⌨️ Hệ thống phím tắt (Hotkeys)

| Phím | Chức năng | Hướng dẫn |
| :--- | :--- | :--- |
| **F6** | **Bắt đầu ghi** | Xóa dữ liệu cũ và bắt đầu ghi lại các thao tác mới. |
| **F7** | **Dừng ghi & Lưu** | Dừng ghi hình và hiện hộp thoại để bạn đặt tên file `.json`. |
| **F8** | **Chạy Macro** | Chọn file macro đã lưu để bắt đầu phát lại tự động. |
| **F9** | **Dừng tất cả** | Dừng ngay lập tức việc ghi hoặc phát macro. |

---

## 🚀 Hướng dẫn cho Người dùng (User)

1. **Giải nén:** Nếu bạn nhận được file `.zip`, hãy giải nén ra một thư mục riêng trước khi dùng.
2. **Quyền Quản trị:** Chuột phải vào file `MacroToolPro.exe` và chọn **Run as Administrator** (Bắt buộc để phần mềm có quyền điều khiển các ứng dụng khác).
3. **Cách dùng:**
   - Nhấn **F6** -> Thực hiện các thao tác máy tính.
   - Nhấn **F7** -> Nhập tên file (ví dụ: `farm_game`) để lưu.
   - Nhập **Số lần lặp** mong muốn vào ô trên tool.
   - Nhấn **F8** -> Chọn file `farm_game.json` để tool bắt đầu chạy.

---

## 🛠 Hướng dẫn tải và cài đặt
### 1. Thư viện cần
Yêu cầu Python 3.10 trở lên. Cài đặt các thư viện bổ trợ:
```bash
pip install pyautogui pynput


### 2. Nếu muốn xuất exe
pip install pyinstaller

# Xuất exe
pyinstaller --noconsole --onefile --collect-all pynput --name "MacroToolPro" --uac-admin marco.py
