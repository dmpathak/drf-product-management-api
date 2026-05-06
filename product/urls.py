from rest_framework.routers import DefaultRouter

from product.views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('product', ProductViewSet, basename='product')

urlpatterns = router.urls
