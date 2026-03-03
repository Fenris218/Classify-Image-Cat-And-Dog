# 🚀 Hướng Dẫn Bắt Đầu Nhanh

## 1️⃣ Tạo Admin Account

```bash
python manage.py createsuperuser
# Nhập username: admin
# Nhập email: admin@dogshop.vn
# Nhập password: (tự chọn)
```

## 2️⃣ Chạy Server

```bash
python manage.py runserver
```

Truy cập: http://localhost:8000/admin

## 3️⃣ Thêm Dữ Liệu Test

### Bước 1: Tạo Giống Chó

1. Đăng nhập Admin: http://localhost:8000/admin
2. Click "Chó Breed" (DogBreeed)
3. Click "Add Dog Breed"
4. Thêm các giống:

```
1. Bulldog
   - Xuất xứ: Anh
   - Đặc điểm: Vóc dáng chắc chắn, khuôn mặt phẳng
   
2. Poodle
   - Xuất xứ: Pháp
   - Đặc điểm: Lông xoăn, thông minh
   
3. Labrador Retriever
   - Xuất xứ: Canada
   - Đặc điểm: Tính tình vui vẻ, dễ huấn luyện
   
4. Golden Retriever
   - Xuất xứ: Anh
   - Đặc điểm: Lông vàng đẹp, tính tình tốt
   
5. Husky
   - Xuất xứ: Nga
   - Đặc điểm: Mắt xanh, năng lượng cao
```

### Bước 2: Tạo Chó Bán

1. Click "Chó" (Dog)
2. Click "Add Dog"
3. Thêm dữ liệu:

```
Ví dụ 1:
- Tên: Max
- Giống: Bulldog
- Tuổi: 12 tháng
- Màu: Trắng-Nâu
- Giá: 50000000
- Người bán: admin (chọn user của bạn)
- Tải ảnh (hoặc bỏ qua)
- Mô tả: Chú Bulldog đẹp, khỏe mạnh

Ví dụ 2:
- Tên: Luna
- Giống: Husky
- Tuổi: 8 tháng
- Màu: Xám-Trắng
- Giá: 40000000
- Người bán: admin
- Mô tả: Cô Husky xinh đẹp với đôi mắt xanh
```

## 4️⃣ Kiểm Tra Website

### Trang Chủ
```
http://localhost:8000/
```

### Danh Sách Chó
```
http://localhost:8000/dogs/
```

### Nhận Diện Giống
```
http://localhost:8000/detect-breed/
```

### Đăng Nhập (Khách Hàng)
```
http://localhost:8000/login/
```
- Username: (tạo tài khoản mới hoặc dùng admin)
- Password: (password bạn chọn)

## 5️⃣ Test Chức Năng E-Commerce

### A. Mua Hàng
1. Đăng nhập (login)
2. Xem danh sách chó → /dogs/
3. Click "Xem Chi Tiết"
4. Click "Thêm Vào Giỏ"
5. Xem giỏ hàng → /cart/
6. Click "Thanh Toán"
7. Điền thông tin giao hàng
8. Nhập thông tin thẻ (test):
   - Số thẻ: 4242 4242 4242 4242
   - Ngày hết hạn: 12/25
   - CVV: 123
9. Click "Thanh Toán"
10. Xem chi tiết đơn hàng

### B. AI Nhận Diện
1. Click "🧠 Nhận Diện Giống" (top nav)
2. Tải ảnh chó lên (hoặc ảnh bất kỳ để test)
3. Click "Nhận Diện"
4. Xem kết quả & gợi ý chó cùng giống

## ⚙️ Cấu Hình MySQL

Nếu cần thay đổi cấu hình database:

**File:** `catdog_project/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'catdog_db',          # Tên database
        'USER': 'root',               # Username MySQL
        'PASSWORD': '123456',         # Password MySQL
        'HOST': 'localhost',          # Server
        'PORT': '3306',               # Port
    }
}
```

## 📸 Thêm Ảnh Chó

1. Tạo thư mục nếu chưa có:
```bash
mkdir media
mkdir media/dogs
mkdir media/uploads
```

2. Copy ảnh vào `media/dogs/`

3. Upload ảnh khi tạo chó trong admin

## 🐛 Troubleshooting

### Lỗi: "Connection refused"
```
→ Kiểm tra MySQL service có chạy không
→ Kiểm tra credentials trong settings.py
```

### Lỗi: "Table does not exist"
```
→ Chạy: python manage.py migrate
```

### Lỗi: "Port 8000 already in use"
```
→ Chạy: python manage.py runserver 8001
```

## ✅ Checklist Bắt Đầu

- [ ] Tạo admin account
- [ ] Chạy server
- [ ] Tạo 5+ giống chó
- [ ] Tạo 3+ chó bán
- [ ] Test mua hàng
- [ ] Test AI detection
- [ ] Xem admin interface

---

**Chúc mừng! 🎉 Project DogShop đã sẵn sàng hoạt động!**
