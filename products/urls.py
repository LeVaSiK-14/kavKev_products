from products.views import CategoryViewSet, ProductsViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('category', CategoryViewSet)
router.register('product', ProductsViewSet)

urlpatterns = []

urlpatterns += router.urls