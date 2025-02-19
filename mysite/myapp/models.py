from django.db import models
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.utils import timezone
from users.models import User  # Предполагается, что модель пользователя находится в приложении users

# Модель категории товаров
class ProductsCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Модель товара (без поля discount)
class Products(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/products', blank=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE, default=1)
    search_vector = SearchVectorField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.search_vector = SearchVector('name', 'description')
        super().save(*args, **kwargs)

    def get_discounted_price(self):
        """
        Рассчитывает цену с учетом активной скидки, если таковая существует.
        Здесь используется обратное отношение к Discount через related_name 'discounts'.
        """
        active_discount = self.discounts.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).first()
        if active_discount:
            return self.price * (1 - active_discount.percent / 100)
        return self.price

    def get_active_discount_end_date(self):
        active_discount = self.discounts.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).first()
        if active_discount:
            return active_discount.end_date
        return None

    def __str__(self):
        return f'{self.name} | {self.category.name}'

# Модель скидки
class Discount(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='discounts')
    code = models.CharField(max_length=50, unique=True)  # Код скидки
    percent = models.DecimalField(max_digits=5, decimal_places=2)  # Процент скидки
    start_date = models.DateTimeField()  # Дата начала действия скидки
    end_date = models.DateTimeField()  # Дата окончания действия скидки
    is_active = models.BooleanField(default=True)  # Активна ли скидка

    def __str__(self):
        return f"Discount for {self.product.name} - {self.percent}%"
    
    def save(self, *args, **kwargs):
        if self.end_date < timezone.now():
            self.is_active = False
        super().save(*args, **kwargs)

# Модель корзины
class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def get_price(self):
        """Возвращает цену товара с учетом скидки через метод get_discounted_price() модели Products"""
        return self.product.get_discounted_price()

    def get_total_price(self):
        """Общая сумма для этой позиции корзины с учетом количества товара и скидки"""
        return self.get_price() * self.quantity

# Модель заказа
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

# Модель деталей заказа
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Order {self.order.id} - {self.product.name} ({self.quantity})'

# Модель рейтинга товара
class ProductRating(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} - {self.user.username}'

    def get_rating_stars(self):
        return range(self.rating)

    def get_empty_stars(self):
        return range(5 - self.rating)
