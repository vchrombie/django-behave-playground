from django.urls import include, path

from rest_framework import routers

from .views import UserViewSet, CartViewSet, DeliveryCostViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'cart', CartViewSet)
router.register(r'delivery-cost', DeliveryCostViewSet)

urlpatterns = [
    path('', include((router.urls, 'cart'))),
]
