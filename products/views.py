from products.models import (
                            Category, 
                            Products, 
                            Raiting, 
                            CartProduct, 
                            Cart,
                            Order)
from products.serializers import (
                            CategorySerializer, 
                            ProductSerializer, 
                            RaitingSerializer,
                            AmountSerializer,
                            CartSerializer,
                            OrderSerializer,
                            RegistrationSerializer)

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import (
                                    RetrieveAPIView)
from rest_framework.views import APIView
from rest_framework.status import (
                                    HTTP_200_OK,
                                    HTTP_400_BAD_REQUEST,
                                    HTTP_201_CREATED,)
from rest_framework.permissions import (
                                    IsAdminUser, 
                                    IsAuthenticated, 
                                    IsAuthenticatedOrReadOnly)

from django_filters import rest_framework as django_filter
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [django_filter.DjangoFilterBackend, SearchFilter]
    search_fields = ['category', ]

    @action(
            methods=['post', ], 
            detail=True, 
            permission_classes = [IsAdminUser, ], 
            serializer_class = ProductSerializer)
    def add_product(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer_class()(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save(category = category)
            return Response(serializer.data, status = HTTP_200_OK)
            

class ProductsViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filter.DjangoFilterBackend, SearchFilter]
    search_fields = ['name_product', ]

    @action(
            methods=['post', ], 
            detail=True, 
            serializer_class = RaitingSerializer, 
            permission_classes=[IsAuthenticated, ])
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



    @action(
        permission_classes = [IsAuthenticated, ],
        serializer_class = AmountSerializer,
        methods = ['post', ],
        detail = True)
    def cart(self, request, *args, **kwargs):
        product = self.get_object()
        cart = request.user.cart

        serializer = AmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        requested_amount = serializer.validated_data.get('amount')

        if request.method == "POST":

            if requested_amount > product.amount:
                return Response(
                            {'Error': 'Requested amount is larger then product amount'},
                            status=HTTP_400_BAD_REQUEST)

            cart_product, created = CartProduct.objects.get_or_create(
                cart=cart,
                product=product)

            if created:

                if requested_amount == 0:
                    return Response({'Error': 'Requested amount is not be zero'})
                else:
                    cart_product.quantity_product = requested_amount
                    cart_product.general_price = (product.price * requested_amount)
                    product.amount -= requested_amount
                    product.save()

            else:

                now_amount = cart_product.quantity_product

                if requested_amount > now_amount:
                    cart_product.quantity_product = requested_amount
                    cart_product.general_price = (product.price * requested_amount)
                    cart_product.save()
                    product.amount -= (requested_amount-now_amount)
                    product.save()
                    genPrice = CartProduct.objects.filter(cart=cart).values_list('general_price', flat=True)
                    genPrice = sum(genPrice)
                    cart.sum_price = genPrice
                    cart.save()
                    serializer = CartSerializer(instance=cart)
                    return Response(serializer.data)

                elif requested_amount == now_amount:
                    genPrice = CartProduct.objects.filter(cart=cart).values_list('general_price', flat=True)
                    genPrice = sum(genPrice)
                    cart.sum_price = genPrice
                    cart.save()
                    serializer = CartSerializer(instance=cart)
                    return Response(serializer.data)

                elif requested_amount == 0:
                    cart_product.delete()
                    product.amount += now_amount
                    product.save()
                    genPrice = CartProduct.objects.filter(cart=cart).values_list('general_price', flat=True)
                    genPrice = sum(genPrice)
                    cart.sum_price = genPrice
                    cart.save()
                    serializer = CartSerializer(instance=cart)
                    return Response(serializer.data)

                else:
                    cart_product.quantity_product = requested_amount
                    cart_product.general_price = (product.price * requested_amount)
                    cart_product.save()
                    product.amount += (now_amount-requested_amount)
                    product.save()
                    genPrice = CartProduct.objects.filter(cart=cart).values_list('general_price', flat=True)
                    genPrice = sum(genPrice)
                    cart.sum_price = genPrice
                    cart.save()
                    serializer = CartSerializer(instance=cart)
                    return Response(serializer.data)

            cart_product.save()
            genPrice = CartProduct.objects.filter(cart=cart).values_list('general_price', flat=True)
            genPrice = sum(genPrice)
            cart.sum_price = genPrice
            cart.save()
            serializer = CartSerializer(instance=cart)
            return Response(serializer.data)

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user)


    @action(
        methods = ['post', ],
        detail = False,
        permission_classes = [IsAuthenticated, ],
        serializer_class = OrderSerializer)
    def create_order(self, request, *args, **kwargs):
        cart = request.user.cart

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cart_data = []
        
        for i in cart.cartproduct_set.all():
            cart_products = {}
            cart_products['id_product'] = i.product.id
            cart_products['name_product'] = i.product.name_product
            cart_products['quantity_product'] = i.quantity_product
            cart_products['general_price'] = i.general_price
            cart_data.append(cart_products)

        order = Order.objects.create(
                                cart=cart,
                                cart_prod=cart_data,
                                sum_price=cart.sum_price,
                                adress=data['adress'],
                                status=data['status'])
        order.save()

        serializer = OrderSerializer(instance=order)

        cart.cart_product.clear()
        cart.sum_price = 0

        cart.save()                

        return Response(serializer.data)


class RegistrationAPIView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'Message': 'User with such username is already exists'})

        user = User.objects.create_user(username=username, password=password)

        token = Token.objects.create(user=user)

        return Response({'token': token.key})

# {
# "username": "levasik",
# "password": "qwerty12345"
# }