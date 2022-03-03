from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User, Cart, DeliveryCost
from .serializers import UserSerializer, CartSerializer, DeliveryCostSerializer
from .helpers import CartHelper


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by('id')
    serializer_class = CartSerializer

    @action(
        methods=['GET', ],
        detail=False,
        url_path='checkout/<user_id>/',
        url_name='checkout'
    )
    def checkout(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=int(kwargs.get('user_id')))
        except Exception as e:
            return Response(
                data={'Error': 'User not found\n' + str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart_helper = CartHelper(user=user)
        checkout_details = cart_helper.prepare_cart_checkout()

        if not checkout_details:
            return Response(
                data={'Error': 'Cart of the User is empty\n'}
            )
        return Response(
            data={'checkout_details': checkout_details}
        )


class DeliveryCostViewSet(viewsets.ModelViewSet):
    queryset = DeliveryCost.objects.all().order_by('id')
    serializer_class = DeliveryCostSerializer
