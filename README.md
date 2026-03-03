# 🐕 DogShop - Website Bán Chó Cảnh Tích Hợp AI

Một nền tảng e-commerce hoàn chỉnh để bán chó cảnh với tích hợp AI nhận diện giống chó.

## ✨ Tính Năng Chính

### 1. **👤 Tài Khoản & Xác Thực**
- ✅ Đăng ký tài khoản mới
- ✅ Đăng nhập / Đăng xuất
- ✅ Quản lý hồ sơ người dùng
- ✅ Tự động tạo giỏ hàng khi đăng ký

### 2. **🐕 Danh Sách Chó & Chi Tiết Sản Phẩm**
- ✅ Xem danh sách tất cả các chó bán
- ✅ Lọc theo giống chó, giá tiền
- ✅ Tìm kiếm theo tên
- ✅ Sắp xếp (mới nhất, giá cao-thấp)
- ✅ Xem chi tiết từng chú chó
- ✅ Thông tin đầy đủ: tuổi, màu sắc, mô tả, giá tiền

### 3. **🛒 Giỏ Hàng & Thanh Toán**
- ✅ Thêm/Xóa sản phẩm khỏi giỏ
- ✅ Xem tóm tắt giỏ hàng
- ✅ Nhập thông tin giao hàng (địa chỉ, điện thoại)
- ✅ Mock thanh toán (hệ thống thử nghiệm)
- ✅ Xác nhận đơn hàng

### 4. **💳 Quản Lý Đơn Hàng**
- ✅ Xem lịch sử đơn hàng
- ✅ Chi tiết đơn hàng
- ✅ Trạng thái đơn hàng (Chờ, Đã thanh toán, Giao hàng, Đã giao)
- ✅ Lịch sử mua hàng

### 5. **🧠 AI Nhận Diện Giống Chó**
- ✅ Tải ảnh lên để nhận diện giống chó
- ✅ Sử dụng Deep Learning Transfer Learning
- ✅ Hiển thị độ tin cây (%)
- ✅ Tự động gợi ý các chú chó cùng giống
- ✅ Hiển thị thông tin giống chó

### 6. **🗄️ Quản Lý Admin**
- ✅ Quản lý giống chó (DogBreed)
- ✅ Quản lý chó bán (Dog)
- ✅ Quản lý đơn hàng
- ✅ Xem lịch sử AI detection
- ✅ Interface Django Admin tích hợp sẵn

## 🔧 Cài Đặt & Chạy Project

### 1. **Yêu Cầu**
```bash
Python 3.8+
MySQL Server (đã cấu hình)
TensorFlow 2.x (cho AI detection)
```

### 2. **Cài Đặt**
```bash
# 1. Clone hoặc vào project
cd d:\Ky6\Python\Django\catdog_project

# 2. Cài đặt dependencies (nếu cần)
pip install django mysql-connector-python tensorflow opencv-python pillow

# 3. Chạy migrations
python manage.py migrate

# 4. Tạo superuser (admin)
python manage.py createsuperuser

# 5. Chạy server
python manage.py runserver
```

### 3. **Truy Cập Website**
- **Trang chủ:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/

## 📋 Cấu Trúc Project

```
catdog_project/
├── catdog_project/          # Cối lõi Django
│   ├── settings.py          # Cấu hình chính
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI app
├── classifier/              # App chính
│   ├── models.py            # Database models
│   ├── views.py             # Business logic
│   ├── urls.py              # URL patterns
│   ├── admin.py             # Admin interface
│   ├── forms.py             # Forms
│   ├── signals.py           # Django signals
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template
│   │   ├── index.html       # Home page
│   │   ├── dogs_list.html   # Dog listing
│   │   ├── dog_detail.html  # Dog detail
│   │   ├── cart.html        # Shopping cart
│   │   ├── checkout.html    # Checkout form
│   │   ├── payment.html     # Payment page
│   │   ├── order_*.html     # Order pages
│   │   └── detect_breed.html # AI detection
│   └── migrations/          # Database migrations
├── media/
│   └── uploads/             # User uploaded files
│   └── dogs/                # Dog images
├── static/                  # Static files
└── manage.py                # Django manage script
```

## 📊 Database Models

### 1. **DogBreed** - Giống chó
```
- name: Tên giống chó
- description: Mô tả
- characteristics: Đặc điểm
- origin: Xuất xứ
```

### 2. **Dog** - Chó bán
```
- breed: FK tới DogBreed
- name: Tên chú chó
- age_months: Tuổi (tháng)
- color: Màu sắc
- price: Giá bán
- image: Ảnh đại diện
- seller: FK tới User
- is_available: Còn bán?
```

### 3. **Cart** - Giỏ hàng
```
- user: FK tới User (OneToOne)
- created_at: Ngày tạo
- updated_at: Cập nhật lần cuối
```

### 4. **Order** - Đơn hàng
```
- user: FK tới User
- status: Trạng thái (pending, paid, shipped, delivered)
- total_price: Tổng tiền
- customer_name: Tên khách hàng
- customer_email: Email
- customer_phone: SĐT
- customer_address: Địa chỉ giao hàng
```

### 5. **PredictionJob** - AI detection job
```
- user: FK tới User
- image: Ảnh upload
- status: queued, running, done, failed
- prediction: Kết quả nhận diện
- confidence: Độ tin cây (0-100)
```

## 🤖 AI Nhận Diện

### Model Hiện Tại
- Sử dụng model `cats_dogs_model.keras` (Transfer Learning)
- Nhận diện: Cat / Dog

### Để Nâng Cấp Thành Nhận Diện Dog Breed
1. Train model mới với dataset các giống chó
2. Lưu vào file `.keras` hoặc `.h5`
3. Cập nhật đường dẫn trong `views.py`:
   ```python
   _MODEL = tf.keras.models.load_model("dog_breed_model.keras")
   _CLASS_NAMES = ["Bulldog", "Poodle", "Labrador", ...]
   ```
4. Cập nhật models để lưu breed info từ Google

## 🔑 Thao Tác Chính

### Cho Người Bán (Admin)
1. Vào http://localhost:8000/admin
2. Tạo giống chó mới (DogBreed)
3. Thêm chú chó mới (Dog)
4. Quản lý đơn hàng, xem trạng thái

### Cho Khách Hàng
1. Đăng ký tài khoản
2. Duyệt danh sách chó
3. Xem chi tiết từng chú chó
4. Thêm vào giỏ hàng
5. Thanh toán & xác nhận
6. Dùng AI để nhận diện giống chó

## 📝 Quy Trình Thêm Chó Mới

```bash
# 1. Vào Django Admin
# 2. Chọn "Chó" (Dogs)
# 3. Nhấp "Thêm chó"
# 4. Điền thông tin:
#    - Tên chú chó
#    - Giống (chọn từ danh sách)
#    - Tuổi (tháng)
#    - Màu sắc
#    - Giá tiền
#    - Tải ảnh lên
#    - Mô tả (tuỳ chọn)
# 5. Chọn người bán (bạn)
# 6. Nhấp "Lưu"
```

## 💳 Mock Payment

Hệ thống thanh toán hiện tại là **mock** (giả định) để thử nghiệm. 

Để sử dụng:
1. Nhập bất kỳ số thẻ nào (VD: 1234567890123456)
2. Nhập bất kỳ CVV nào (VD: 123)
3. Đơn hàng sẽ được xác nhận

### Để Tích Hợp Thanh Toán Thực
- Sử dụng Stripe, PayPal, hoặc VNPay API
- Cập nhật view `payment_view` trong `views.py`

## 🔐 Bảo Mật

⚠️ **LƯU Ý**: Project hiện đang trong chế độ **DEV** (DEBUG = True)

Để sản xuất (production):
1. Đặt `DEBUG = False` trong `settings.py`
2. Đổi `SECRET_KEY` thành key bảo mật
3. Cấu hình ALLOWED_HOSTS
4. Sử dụng HTTPS
5. Thiết lập mật khẩu database an toàn

## 📚 Công Nghệ Sử Dụng

- **Backend:** Django 4.2.8
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript
- **ML/AI:** TensorFlow, Keras, OpenCV
- **Image Storage:** Django FileField + Pillow

## 🎯 Tính Năng Sắp Tới

- [ ] Quên mật khẩu & Reset password
- [ ] Tích hợp thanh toán thực (Stripe/PayPal/VNPay)
- [ ] Hệ thống đánh giá & bình luận
- [ ] Tìm kiếm nâng cao
- [ ] Mobile app (React Native)
- [ ] Email notifications
- [ ] Lịch giao hàng real-time

## 📞 Hỗ Trợ

- **Email:** info@dogshop.vn
- **Hotline:** 0123-456-789
- **Website:** (sắp ra mắt)

---

**© 2026 DogShop - Bán Chó Cảnh Hàng Đầu Việt Nam** 🐕
