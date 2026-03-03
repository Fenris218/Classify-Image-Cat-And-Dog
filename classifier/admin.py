from django.contrib import admin
from .models import DogBreed, Dog, Cart, CartItem, Order, OrderItem, UploadedImage, PredictionJob

# ==================== DOG BREEDS ====================
@admin.register(DogBreed)
class DogBreedAdmin(admin.ModelAdmin):
    list_display = ['name', 'origin']
    search_fields = ['name', 'origin']
    list_filter = ['origin']


# ==================== DOG LISTINGS ====================
@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'age_months', 'price', 'seller', 'is_available', 'created_at']
    list_filter = ['breed', 'is_available', 'created_at']
    search_fields = ['name', 'breed__name', 'seller__username']
    readonly_fields = ['created_at', 'updated_at']


# ==================== SHOPPING CART ====================
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_price', 'updated_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]


# ==================== ORDERS ====================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'customer_name', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]


# ==================== AI DETECTION ====================
@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'prediction', 'confidence', 'uploaded_at']
    list_filter = ['prediction', 'uploaded_at']
    search_fields = ['user__username', 'prediction']
    readonly_fields = ['uploaded_at']


@admin.register(PredictionJob)
class PredictionJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'prediction', 'confidence', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'prediction']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
