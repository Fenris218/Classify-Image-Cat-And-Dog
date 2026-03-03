from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ==================== DOG BREED ==================== 
class DogBreed(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    characteristics = models.TextField(blank=True, help_text="Đặc điểm giống chó")
    origin = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# ==================== DOG LISTING ==================== 
class Dog(models.Model):
    breed = models.ForeignKey(DogBreed, on_delete=models.CASCADE, related_name='dogs')
    name = models.CharField(max_length=100)
    age_months = models.IntegerField(help_text="Tuổi tính bằng tháng")
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='dogs/')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dogs_for_sale')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.breed.name}) - {self.price}đ"

    class Meta:
        ordering = ['-created_at']


# ==================== SHOPPING CART ==================== 
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total_price(self):
        return sum([item.get_total_price() for item in self.items.all()])

    def get_total_items(self):
        return sum([item.quantity for item in self.items.all()])


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dog.name} x {self.quantity}"

    def get_total_price(self):
        return self.dog.price * self.quantity


# ==================== ORDERS ==================== 
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Đang chờ'),
        ('paid', 'Đã thanh toán'),
        ('shipped', 'Đang giao'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dog = models.ForeignKey(Dog, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá tại thời điểm đặt hàng
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.dog.name if self.dog else 'Deleted'} - Order #{self.order.id}"


# ==================== AI BREED DETECTION ==================== 
class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    prediction = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prediction}"


class PredictionJob(models.Model):
    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("running", "Running"),
        ("done", "Done"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="queued")
    prediction = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
