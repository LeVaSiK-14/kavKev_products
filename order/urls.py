from rest_framework.routers import SimpleRouter
from order.views import OrderViewSet

router = SimpleRouter()
router.register('order', OrderViewSet)

urlpatterns = []
urlpatterns += router.urls