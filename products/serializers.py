from products.models import Category, Products

from rest_framework.serializers import ModelSerializer


class ProductSerializer(ModelSerializer):
    
    class Meta:
        model = Products
        fields = ['category', 'name_product', 'composition', 'price', 'inStock', 'articul']
        read_only_fields = ['category',]

        
class CategorySerializer(ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category', 'products']

