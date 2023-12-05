from django.db import models

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
    category = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE, default=1)  # Установите значение по умолчанию для категории

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

class ProductRating(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  # Предполагается, что рейтинг может быть целым числом от 0 до 5

    def get_rating_stars(self):
        return range(1, self.rating + 1)

    def get_empty_stars(self):
        return range(self.rating + 1, 6 - self.rating)
