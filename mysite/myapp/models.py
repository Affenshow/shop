from django.db import models
from django.contrib.postgres.search import SearchVectorField
from users.models import User

class ProductsCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/products', blank=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE, default=1)
    # Добавляем поле для поиска
    search_vector = SearchVectorField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Обновляем поле search_vector при сохранении
        self.search_vector = SearchVector('name', 'description')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} | {self.category.name}'
    
class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.products.name}'
    
    def sum(self):
        return self.quantity * self.product.price
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Products', through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Order {self.order.id} - {self.product.name} ({self.quantity})'
    
    

class ProductRating(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} - {self.user.username}'

    def get_rating_stars(self):
        return range(self.rating)

    def get_empty_stars(self):
        return range(5 - self.rating)
