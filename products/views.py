from products.models import Category
from products.serializers import CategorySerializer, ProductSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as django_filter
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [django_filter.DjangoFilterBackend, SearchFilter]
    search_fields = ['name_product', ]

    @action(methods=['post', ], detail=True, permission_classes = [IsAdminUser, ], serializer_class = ProductSerializer)
    def add_product(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(category=category)
            return Response(serializer.data, status =HTTP_200_OK)

