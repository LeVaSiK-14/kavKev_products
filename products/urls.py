from products.views import CategoryViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('category', CategoryViewSet)

urlpatterns = []

urlpatterns += router.urls