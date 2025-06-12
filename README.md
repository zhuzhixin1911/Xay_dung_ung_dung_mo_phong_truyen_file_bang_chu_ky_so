# -*- coding: utf-8 -*-

# Nội dung đầy đủ cho tệp README.md được lưu trong một chuỗi nhiều dòng
readme_content = """
# Công cụ Ký và Xác thực Chữ ký số cho Tài liệu

Dự án này cung cấp một bộ hai công cụ dựa trên web được xây dựng bằng Python, Flask và thư viện `cryptography` để minh họa quá trình tạo và xác thực chữ ký số cho tài liệu.

1.  **Trình Tạo Chữ Ký Số (`generator.py`):** Một ứng dụng web cho phép người dùng tải lên một tài liệu, sau đó tạo ra một cặp khóa (công khai và bí mật), mã băm (hash) của tài liệu, và chữ ký số tương ứng.
2.  **Trình Xác Thực Chữ Ký Số (`verifier.py`):** Một ứng dụng web dùng để xác thực tính toàn vẹn và nguồn gốc của tài liệu. Người dùng cần cung cấp tài liệu gốc, chữ ký số và khóa công khai để kiểm tra.

Cả hai ứng dụng đều sử dụng `pyngrok` để tạo một đường hầm (tunnel) công khai, giúp bạn có thể truy cập chúng từ bất kỳ đâu qua Internet một cách dễ dàng.

## ✨ Các Khái niệm Cốt lõi

-   **Mã Băm (Hash):** Một chuỗi ký tự có độ dài cố định được tạo ra từ dữ liệu đầu vào (nội dung tài liệu). Thuật toán được sử dụng ở đây là SHA-256. Bất kỳ thay đổi nhỏ nào trong tài liệu cũng sẽ tạo ra một mã băm hoàn toàn khác.
-   **Khóa Bí Mật (Private Key):** Một khóa mã hóa mà chỉ người chủ sở hữu biết. Nó được dùng để *tạo* ra chữ ký số. **Tuyệt đối không được chia sẻ khóa này**.
-   **Khóa Công Khai (Public Key):** Một khóa được chia sẻ công khai cho bất kỳ ai. Nó được dùng để *xác thực* chữ ký số đã được tạo bằng khóa bí mật tương ứng.
-   **Chữ Ký Số (Digital Signature):** Dữ liệu được tạo ra bằng cách dùng **Khóa Bí Mật** để mã hóa **Mã Băm** của tài liệu. Chữ ký này chứng minh rằng người sở hữu khóa bí mật đã ký vào tài liệu và tài liệu không bị thay đổi kể từ khi ký.

## 🚀 Tính năng chính

-   Giao diện web đơn giản và trực quan.
-   Tạo cặp khóa RSA (2048-bit) một cách tự động.
-   Băm tài liệu bằng thuật toán an toàn SHA-256.
-   Ký tài liệu bằng Khóa Bí mật với đệm PSS (Probabilistic Signature Scheme) để tăng cường bảo mật.
-   Xác thực chữ ký dựa trên tài liệu gốc, chữ ký và Khóa Công khai.
-   Tự động tạo URL công khai bằng Ngrok.

## 📋 Hướng dẫn Cài đặt và Sử dụng

### 1. Điều kiện tiên quyết

-   Python 3.6 trở lên.
-   `pip` (trình quản lý gói của Python).
-   Tài khoản Ngrok để lấy Authtoken.

### 2. Lấy Ngrok Authtoken

1.  Đăng ký tài khoản miễn phí tại [dashboard.ngrok.com](https://dashboard.ngrok.com/signup).
2.  Sau khi đăng nhập, truy cập vào mục [Your Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken).
3.  Sao chép token của bạn.

### 3. Cài đặt

1.  **Tạo thư mục cho dự án:**
    ```bash
    mkdir digital-signature-tool
    cd digital-signature-tool
    ```

2.  **Lưu mã nguồn:**
    * Lưu đoạn mã "Trình Tạo Chữ Ký Số" vào một tệp có tên `generator.py`.
    * Lưu đoạn mã "Trình Xác Thực Chữ Ký Số" vào một tệp có tên `verifier.py`.

3.  **Cấu hình Ngrok Authtoken:**
    * Mở cả hai tệp `generator.py` và `verifier.py`.
    * Tìm dòng sau và thay thế `YOUR_NGROK_AUTH_TOKEN` bằng token thật của bạn:
        ```python
        NGROK_AUTH_TOKEN = "YOUR_NGROK_AUTH_TOKEN" #<-- THAY TOKEN CỦA BẠN VÀO ĐÂY
        ```

4.  **Cài đặt các thư viện cần thiết:**
    Chạy lệnh sau trong terminal hoặc command prompt:
    ```bash
    pip install flask pyngrok cryptography
    ```

### 4. Quy trình làm việc

#### Bước 1: Tạo Chữ ký số

1.  Chạy ứng dụng tạo chữ ký:
    ```bash
    python generator.py
    ```
2.  Terminal sẽ hiển thị một URL công khai từ Ngrok. Ví dụ:
    ```
    * Trang web của bạn đang chạy tại: https://<random-string>.ngrok-free.app
    ```
3.  Mở URL này trong trình duyệt của bạn.
4.  Nhấp vào "Chọn tệp..." và tải lên tài liệu bạn muốn ký.
5.  Trang web sẽ tự động xử lý và hiển thị:
    * **Khóa Công khai (Public Key)**
    * **Khóa Bí mật (Private Key)**
    * **Mã Băm (SHA-256 Hash) của Tài liệu**
    * **Chữ ký số (Signature)**
6.  **Sao chép và lưu lại cẩn thận** Khóa Công khai và Chữ ký số. Bạn sẽ cần chúng để xác thực.

> **Lưu ý quan trọng:** Hãy cất giữ Khóa Bí mật ở một nơi an toàn. Trong ứng dụng này, mỗi lần bạn tải tệp lên, một cặp khóa mới sẽ được tạo ra.

#### Bước 2: Xác thực Chữ ký số

1.  Mở một cửa sổ terminal mới (giữ nguyên terminal cũ đang chạy `generator.py`).
2.  Chạy ứng dụng xác thực:
    ```bash
    python verifier.py
    ```
3.  Một URL Ngrok mới sẽ được tạo cho trình xác thực. Mở URL này trong trình duyệt.
4.  Trên trang xác thực, bạn cần cung cấp 3 thông tin:
    * **Tải lên tệp gốc:** Tải lên chính xác tệp bạn đã dùng để tạo chữ ký ở Bước 1.
    * **Dán chữ ký số:** Dán chuỗi Chữ ký số (dạng hex) bạn đã sao chép từ trình tạo.
    * **Dán nội dung khóa công khai:** Dán toàn bộ nội dung Khóa Công khai (bắt đầu bằng `-----BEGIN PUBLIC KEY-----` và kết thúc bằng `-----END PUBLIC KEY-----`).
5.  Nhấp vào nút **"Xác thực"**.
6.  Kết quả sẽ được hiển thị:
    * `✅ Xác thực thành công! Đây là chữ ký hợp lệ.` nếu mọi thông tin đều khớp.
    * `❌ Xác thực không thành công! Chữ ký không khớp với tệp.` nếu tài liệu đã bị thay đổi hoặc chữ ký/khóa công khai không đúng.

## ⚠️ Khuyến cáo Bảo mật

-   **Mục đích giáo dục:** Công cụ này được tạo ra chủ yếu cho mục đích học tập và minh họa. **KHÔNG** sử dụng nó cho các ứng dụng thực tế, nhạy cảm về bảo mật mà không có sự kiểm định và cải tiến chuyên sâu.
-   **Quản lý khóa:** Trong thực tế, việc tạo và quản lý khóa cần tuân theo các quy trình bảo mật nghiêm ngặt. Khóa bí mật không bao giờ được hiển thị hoặc truyền đi một cách không an toàn như trong ví dụ này.
-   **Giới hạn của Ngrok:** Phiên bản miễn phí của Ngrok có thể có các giới hạn về băng thông và thời gian hoạt động. Đường hầm sẽ bị đóng khi bạn dừng ứng dụng.
"""

# Tên tệp sẽ được tạo
file_name = "README.md"

try:
    # Mở tệp ở chế độ ghi ('w') với mã hóa utf-8 để hỗ trợ tiếng Việt và các ký tự đặc biệt
    with open(file_name, "w", encoding="utf-8") as file:
        # Ghi nội dung vào tệp
        file.write(readme_content)
    
    print(f"✅ Tệp '{file_name}' đã được tạo và ghi nội dung thành công!")

except IOError as e:
    print(f"❌ Đã xảy ra lỗi khi ghi tệp: {e}")
