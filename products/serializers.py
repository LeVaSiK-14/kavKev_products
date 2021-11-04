from django.core import exceptions
from products.models import Category, Products, Raiting, CartProduct, Cart, Order

from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from rest_framework import exceptions

class RaitingSerializer(ModelSerializer):
    class Meta:

        model = Raiting
        fields = ['appraiser', 'star', 'product']
        read_only_fields = ['appraiser', 'product']


class ProductSerializer(ModelSerializer):


    class Meta:
        model = Products
        fields = ['id', 'category', 'name_product', 'amount', 'composition', 'price', 'inStock', 'articul', 'raiting_general']
        read_only_fields = ['category','raiting_general']
        


class CategorySerializer(ModelSerializer):

    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category', 'products']



class CartProductSerializer(ModelSerializer):
    name_product = serializers.ReadOnlyField(source='product.name_product')
    class Meta:
        model = CartProduct
        fields = ['id', 'name_product', 'quantity_product', 'general_price', ]
        read_only_fields = ['name_product', 'quantity_product', 'general_price', ]


class CartSerializer(ModelSerializer):

    all_products = CartProductSerializer(source='cartproduct_set', many=True, read_only=True)
    author = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Cart
        fields = ['id', 'author', 'all_products', 'sum_price', ]
        read_only_fields = ['sum_price', 'all_products']



class AmountSerializer(Serializer):

    amount = serializers.IntegerField()



class OrderSerializer(ModelSerializer):

    cart = CartSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'cart', 'sum_price', 'cart_prod', 'created_at', 'adress', 'status', ]
        read_only_fields = ['cart', 'sum_price', 'created_at', 'cart_prod', ]


class RegistrationSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validated_password(self, value):
        if len(value) < 5:
            raise exceptions.ValidationError('Password is too short')
        elif len(value) > 20:
            raise exceptions.ValidationError('Password is too long')
        return value