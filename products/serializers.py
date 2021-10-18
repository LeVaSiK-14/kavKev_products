from rest_framework.fields import ReadOnlyField
from products.models import Category, Products, Raiting, CartProduct, Cart, Order

from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

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

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity_product', 'general_price', ]
        read_only_fields = ['product', 'quantity_product', 'general_price', ]


class CartSerializer(ModelSerializer):


    # product = serializers.ReadOnlyField(source='cart_product.product')
    cart_product = CartProductSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Cart
        fields = ['id', 'author', 'cart_product', 'sum_price', ]
        read_only_fields = ['sum_price', 'cart_product']



class AmountSerializer(Serializer):
    
    amount = serializers.IntegerField()