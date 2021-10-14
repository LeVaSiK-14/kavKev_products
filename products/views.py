from products.models import Category, Products, Raiting, CartProduct, Cart, Order
from products.serializers import CategorySerializer, ProductSerializer, RaitingSerializer, CartProductSerializer, CartSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as django_filter
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [django_filter.DjangoFilterBackend, SearchFilter]
    search_fields = ['category', ]

    @action(methods=['post', ], detail=True, permission_classes = [IsAdminUser, ], serializer_class = ProductSerializer)
    def add_product(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(category=category)
            return Response(serializer.data, status =HTTP_200_OK)
            

class ProductsViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filter.DjangoFilterBackend, SearchFilter]
    search_fields = ['name_product', ]

    @action(methods=['post', ], detail=True, serializer_class = RaitingSerializer, permission_classes=[IsAuthenticated, ])
    def add_raiting(self, request, *args, **kwargs):
        product = self.get_object()
        appraiser = request.user
        serializer = RaitingSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            raiting = Raiting.objects.filter(appraiser_id=appraiser.id, product_id=product.id).first()
            if raiting:
                raiting.star = data['star']
                raiting.save()
            else:
                raiting = Raiting.objects.create(
                    appraiser=appraiser,
                    star = data['star'],
                    product = product
                )
                raiting.save()
            p = product.raitings.all().values_list('star__value', flat=True)
            len_arr = len(p)
            sum_arr = sum(p)
            fin_raiting = sum_arr/len_arr
            product.raiting_general=round(fin_raiting, 1)
            product.save()
            serializer = ProductSerializer(instance=product)

            return Response(serializer.data)
        else:
            return Response(serializer.errors)



    # @action(methods=['post', ], detail=True)
    # def add_in_cart(self, request, *args, **kwargs):
    #     product = self.get_object()
    #     customer = request.user

    #     cartProd = CartProduct.objects.filter(customer_id=customer.id, product_id=product.id).first()
    #     if bool(cartProd):
    #         cartProd.quantity_product += 1
    #         cartProd.general_price += product.price
    #         cartProd.save()
    #         cart = Cart.objects.get(customer=customer)
    #         cart.cart_product.add(cartProd)
    #         cart.save()
    #     else:
    #         cartProd = CartProduct.objects.create(
    #                                         product=product, 
    #                                         quantity_product=1,
    #                                         general_price=product.price,
    #                                         customer=customer)
    #         cart = Cart.objects.create(customer=customer, sum_price=product.price)
    #         cart.save()
    #         cart.cart_product.add(cartProd)
    #         cart.save()
    #     serializer = CartSerializer(instance=cart)
    #     return Response(serializer.data)

    @action(methods=['get', 'post',], detail=True, permission_classes=[IsAuthenticated, ])
    def add_in_cart(self, request, *args, **kwargs):
        product = self.get_object()
        customer = request.user
        cart = Cart.objects.create(
                                customer=customer,
                                sum_price=0)
        cart.save()
        cart_product = CartProduct.objects.create(
                                                cart=cart,
                                                product=product,
                                                quantity_product=1,
                                                general_price=product.price,
                                                )
        serializer = CartSerializer(instance=cart)
        return Response(serializer.data)