from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Sum

from django.db.models.signals import post_save
from django.dispatch import receiver

class UserTypes(models.TextChoices):
    Buyer = "buyer", "Buyer"
    Seller = "seller", "Seller"

class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=UserTypes, default=UserTypes.Buyer)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True) 


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_cart")
    is_ordered=models.BooleanField(default=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        
        user_cart = Cart.objects.get(user=self.user)
        user_cart.is_ordered = True
        user_cart.save()

@receiver(post_save, sender=Order)
def update_daily_data(sender, instance, created, **kwargs):
    if created:
        # Calculate revenue for today
        today_revenue = Order.objects.filter(created_at__date=timezone.now().date()).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
        
        # Save or update daily revenue data
        daily_data, _ = DailyData.objects.get_or_create(date=timezone.now().date())
        if today_revenue is not None:  # Check if revenue is not None
            daily_data.revenue = today_revenue  # Set the revenue field
            daily_data.save()
        else:
            # Handle case where revenue is None
            # For example, you could set a default value or log the issue
            pass


class DailyData(models.Model):
    date = models.DateField(unique=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.revenue}"
