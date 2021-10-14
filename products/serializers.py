from products.models import Category, Products, Raiting, CartProduct, Cart, Order

from rest_framework.serializers import ModelSerializer

class RaitingSerializer(ModelSerializer):
    class Meta:

        model = Raiting
        fields = ['appraiser', 'star', 'product']
        read_only_fields = ['appraiser', 'product']


class ProductSerializer(ModelSerializer):


    class Meta:
        model = Products
        fields = ['id', 'category', 'name_product', 'composition', 'price', 'inStock', 'articul', 'raiting_general']
        read_only_fields = ['category','raiting_general']
        



class CategorySerializer(ModelSerializer):

    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category', 'products']



class CartSerializer(ModelSerializer):
    # cart_product = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'cart_product', 'sum_price']
        read_only_fields = ['customer', 'cart_product', 'sum_price']

class CartProductSerializer(ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity_product', 'general_price', 'customer']
        read_only_fields = ['product', 'quantity_product', 'general_price', 'customer']