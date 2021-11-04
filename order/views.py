from rest_framework.viewsets import ModelViewSet
from products.models import Order
from products.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    @action(methods=['get', 'post', ], detail=True, )
    def order_status_success(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user
        if order.cart.customer == user:
            order.status = 'Успешно доставлен'
            order.save()

            return Response({'Status': 'Успешно доставлен'})


    @action(methods=['get', 'post', ], detail=True, )
    def order_status_cancel(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user
        if order.cart.customer == user:
            order.status = 'Отменён'
            order.save()


            return Response({'Status': 'Отменён'})