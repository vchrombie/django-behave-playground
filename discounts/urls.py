from django.urls import include, path

from rest_framework import routers

from .views import CampaignViewSet, CouponViewSet

router = routers.DefaultRouter()
router.register(r'campaign', CampaignViewSet)
router.register(r'coupon', CouponViewSet)

urlpatterns = [
    path('', include((router.urls, 'discounts'))),
]
