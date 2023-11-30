from rest_framework import serializers

from apps.account.models import User
from apps.product.models import Product


class ProductSerializer(serializers.ModelSerializer):

    # Show category titles instead of ID
    def get_category(self, obj: Product):
        return list(obj.category.values_list('title', flat=True))

    category = serializers.SerializerMethodField('get_category')

    # Show brand title instead of ID
    def get_brand(self, obj: Product):
        return obj.brand.title

    brand = serializers.SerializerMethodField('get_brand')

    class Meta:
        model = Product
        exclude = ['image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class BrandSerializer(serializers.ModelSerializer): # Make nested wirtable for category and brand
#     class Meta:
#         model = ProductBrand
#         fields = ['id', 'title']
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductCategory
#         fields = ['id', 'title']
