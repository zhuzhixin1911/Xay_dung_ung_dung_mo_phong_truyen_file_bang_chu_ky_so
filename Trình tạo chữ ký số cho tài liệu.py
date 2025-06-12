#@title Trình Tạo Chữ Ký Số Cho Tài Liệu
# Cấu hình ngrok với token của bạn
# Thay 'YOUR_NGROK_AUTH_TOKEN' bằng token ngrok thực tế của bạn
NGROK_AUTH_TOKEN = "2vQiHuSkEACuMQdfLaOTROncorU_3gmW5HFXANyHBHUfm2ufF" #<-- THAY TOKEN CỦA BẠN VÀO ĐÂY
conf.get_default().auth_token = NGROK_AUTH_TOKEN

# Bước 1: Cài đặt các thư viện cần thiết
!pip install flask pyngrok cryptography -q

import os
import hashlib
from flask import Flask, request, render_template_string
from pyngrok import ngrok, conf
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# --- Cấu hình ngrok ---
if NGROK_AUTHTOKEN:
  conf.get_default().auth_token = NGROK_AUTHTOKEN
else:
  print("CẢNH BÁO: Bạn chưa nhập Ngrok Authtoken. Đường hầm có thể có giới hạn.")

# --- Thiết lập ứng dụng Flask ---
app = Flask(__name__)

# --- Mã HTML và CSS cho giao diện trang web ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Công cụ Ký số Tài liệu</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background-color: #f0f2f5; color: #1c1e21; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); padding: 28px; max-width: 800px; width: 100%; }
        h1 { color: #1877f2; text-align: center; margin-bottom: 24px; font-size: 24px; }
        form { display: flex; flex-direction: column; gap: 16px; }
        .file-upload-wrapper { border: 2px dashed #ccd0d5; border-radius: 8px; padding: 20px; text-align: center; cursor: pointer; transition: background-color 0.2s, border-color 0.2s; }
        .file-upload-wrapper:hover { background-color: #f7f8fa; border-color: #8a9ba8; }
        .file-upload-wrapper p { margin: 0; font-size: 16px; color: #606770; }
        input[type="file"] { display: none; }
        button { background-color: #1877f2; color: white; border: none; border-radius: 6px; padding: 12px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background-color 0.2s; }
        button:hover { background-color: #166fe5; }
        .result { margin-top: 28px; }
        h2 { color: #4b4f56; border-bottom: 1px solid #dddfe2; padding-bottom: 8px; font-size: 18px; }
        pre { background-color: #f0f2f5; padding: 12px; border-radius: 6px; white-space: pre-wrap; word-wrap: break-word; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; font-size: 14px; color: #333; }
        .key-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .key-box { display: flex; flex-direction: column; }
        label { font-weight: bold; margin-bottom: 8px; font-size: 14px; color: #606770;}
    </style>
</head>
<body>
    <div class="container">
        <h1>🖋️ Công cụ Ký số Tài liệu</h1>
        <form method="post" enctype="multipart/form-data">
            <label for="file-upload" class="file-upload-wrapper">
                <p>Nhấp vào đây để chọn tệp từ máy tính</p>
                <input id="file-upload" type="file" name="file" onchange="this.form.submit()">
            </label>
            <button type="button" onclick="document.getElementById('file-upload').click()">Chọn tệp...</button>
        </form>

        {% if result %}
        <div class="result">
            <h2>Kết quả Ký số</h2>
            <div class="key-pair">
                <div class="key-box">
                    <label>🔑 Khóa Công khai (Public Key):</label>
                    <pre>{{ result.public_key }}</pre>
                </div>
                <br>
                <div class="key-box">
                    <label>🔒 Khóa Bí mật (Private Key):</label>
                    <pre>{{ result.private_key }}</pre>
                </div>
            </div>
            <div>
                <label>📄 Mã Băm (SHA-256 Hash) của Tài liệu:</label>
                <pre>{{ result.file_hash }}</pre>
            </div>
            <div>
                <label>✍️ Chữ ký số (Signature):</label>
                <pre>{{ result.signature }}</pre>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# --- Định tuyến và logic xử lý ---
@app.route('/', methods=['GET', 'POST'])
def sign_document():
    if request.method == 'POST':
        # Kiểm tra xem có file được tải lên không
        if 'file' not in request.files:
            return render_template_string(HTML_TEMPLATE, error="Không có tệp nào được chọn!")
        file = request.files['file']
        if file.filename == '':
            return render_template_string(HTML_TEMPLATE, error="Không có tệp nào được chọn!")

        # Đọc nội dung file
        file_content = file.read()

        # 1. Tạo cặp khóa RSA (Công khai và Bí mật)
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()

        # Chuyển đổi khóa sang định dạng PEM để hiển thị
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        # 2. Băm tài liệu bằng thuật toán SHA-256
        file_hash = hashlib.sha256(file_content).hexdigest()

        # 3. Ký vào mã băm bằng khóa bí mật (Tạo chữ ký số)
        signature = private_key.sign(
            file_content, # Ký trực tiếp trên nội dung file
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Chuyển chữ ký sang định dạng hex để dễ đọc
        signature_hex = signature.hex()

        # Chuẩn bị kết quả để hiển thị
        result_data = {
            "public_key": pem_public_key,
            "private_key": pem_private_key,
            "file_hash": file_hash,
            "signature": signature_hex
        }

        return render_template_string(HTML_TEMPLATE, result=result_data)

    # Hiển thị trang ban đầu nếu là phương thức GET
    return render_template_string(HTML_TEMPLATE, result=None)

# --- Khởi chạy web server và ngrok ---
if __name__ == '__main__':
    # Đóng các tunnel ngrok đang chạy nếu có
    try:
      ngrok.kill()
    except:
      pass
    # Mở một tunnel HTTP tới cổng 5000
    public_url = ngrok.connect(5000)
    print(f"🌍 Trang web của bạn đang chạy tại: {public_url}")
    # Chạy ứng dụng Flask
    app.run(port=5000)
