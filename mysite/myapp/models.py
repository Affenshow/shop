from django.db import models

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
        return self.name

class ProductRating(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)  # Предполагается, что рейтинг может быть целым числом от 0 до 5