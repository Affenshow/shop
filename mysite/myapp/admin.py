from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Products, ProductsCategory, Basket,
    ProductRating, Order, OrderItem,
    Discount, Feedback, Review
)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display    = ('name', 'email', 'created', 'responded')
    list_filter     = ('responded', 'created')
    search_fields   = ('name', 'email', 'message', 'response')
    readonly_fields = ('created',)

    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'message', 'created')
        }),
        ('Ответ клиенту', {
            'fields': ('response', 'responded')
        }),
    )

    actions = ['send_response']

    def send_response(self, request, queryset):
        for fb in queryset:
            if fb.response and not fb.responded:
                send_mail(
                    subject=f"Ответ на ваше обращение",
                    message=fb.response,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[fb.email],
                )
                fb.responded = True
                fb.save()
        self.message_user(request, "Ответы отправлены клиентам.")
    send_response.short_description = "Отправить ответ выбранным"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display   = ('product', 'user', 'rating', 'created')
    list_filter    = ('rating', 'created')
    search_fields  = ('product__name', 'user__username', 'comment')

# Регистрируем остальные модели
admin.site.register(Products)
admin.site.register(ProductsCategory)
admin.site.register(Basket)
admin.site.register(ProductRating)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Discount)
