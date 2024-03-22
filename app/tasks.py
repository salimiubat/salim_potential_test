

from celery import shared_task
from datetime import datetime, timedelta
from django.db.models import Sum
from .models import Order, DailyData

# @shared_task
# def update_daily_revenue():
    
#     end_date = datetime.now()
#     start_date = end_date - timedelta(days=1)

#     orders = Order.objects.filter(created_at__range=(start_date, end_date))

#     total_revenue = orders.aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0

#     daily_data, created = DailyData.objects.get_or_create(date=datetime.now().date())
#     daily_data.revenue = total_revenue
#     daily_data.save()

# app/tasks.py
# mysite/app/tasks.py

# tasks.py

from celery import shared_task
from django.utils import timezone
from django.db.models import Sum
from .models import Order, DailyData

# @shared_task
# def calculate_daily_revenue():
#     # Calculate daily revenue
#     now = timezone.now()
#     start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
#     end_of_yesterday = start_of_today - timezone.timedelta(seconds=1)
#     start_of_yesterday = end_of_yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
#     daily_revenue = Order.objects.filter(created_at__gte=start_of_yesterday, created_at__lte=end_of_yesterday).aggregate(Sum('total_amount'))['total_amount__sum']
#     if daily_revenue is None:
#         daily_revenue = 0

#     # Save daily revenue data
#     yesterday_date = start_of_yesterday.date()
#     daily_data, created = DailyData.objects.get_or_create(date=yesterday_date)
#     daily_data.revenue = daily_revenue
#     daily_data.save()


@shared_task
def calculate_daily_revenue():
    # Calculate daily revenue
    now = timezone.now()
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_yesterday = start_of_today - timezone.timedelta(seconds=1)
    start_of_yesterday = end_of_yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    daily_revenue = Order.objects.filter(created_at__gte=start_of_yesterday, created_at__lte=end_of_yesterday).aggregate(Sum('total_amount'))['total_amount__sum']
    if daily_revenue is None:
        daily_revenue = 0

    # Save daily revenue data
    yesterday_date = start_of_yesterday.date()
    daily_data, created = DailyData.objects.get_or_create(date=yesterday_date)
    daily_data.revenue = daily_revenue
    daily_data.save()
