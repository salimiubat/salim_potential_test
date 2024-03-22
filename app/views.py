from rest_framework import viewsets
from .models import *
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.response import Response
from django.views.generic import ListView
from rest_framework.exceptions import PermissionDenied
from rest_framework import status



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
    
        return CartItem.objects.filter(cart__user=user, cart__is_ordered=False)
    
    def perform_create(self, serializer):
        user = self.request.user
        user_cart = Cart.objects.get(user=user, is_ordered=False)
        serializer.save(cart=user_cart)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = self.perform_update(serializer)
        return Response(serializer.data)
    
  
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user, items__cart__is_ordered=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DailyDataViewSet(viewsets.ModelViewSet):
    queryset = DailyData.objects.all()
    serializer_class = DailyDataSerializer # Auto create by celery






class ProductListView(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'
    paginate_by = 12  

    def get_queryset(self):
        return Product.objects.all()