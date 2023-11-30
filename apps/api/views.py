from django.http import HttpRequest

from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsStaffOrReadOnly
from .serializers import UserSerializer, ProductSerializer

from apps.account.models import User
from apps.product.models import Product


class ProductList(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'brand', 'category', 'in_stock']
    search_fields = ['title', 'brand__title', 'category__title', 'description']


class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]


class UserList(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'gender']


class UserDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RevokeToken(APIView):
    def delete(self, request: HttpRequest):
        self.request.auth.delete()
        # When token revoked, show 204 status code (DELETE Method)
        return Response(status=204)
