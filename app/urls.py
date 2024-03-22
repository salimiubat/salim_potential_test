from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register('cartitems', CartItemViewSet,basename="cartitems")
router.register('orders', OrderViewSet,basename="orders")
router.register(r'dailydata', DailyDataViewSet)

urlpatterns = [
    path('ecom/', include(router.urls)),
    path('', ProductListView.as_view(),name="product_list"),


    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
