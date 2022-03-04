from django.db import models
from django.contrib.auth.models import AbstractUser

from products.models import Product


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', )


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, )
    item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, )

    quantity = models.IntegerField(verbose_name='Item', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', )

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(
            self.user,
            self.item,
            self.quantity,
            self.created_at,
            self.updated_at,
        )

    class Meta:
        verbose_name_plural = 'Carts'


class DeliveryCost(models.Model):
    status = models.CharField(
        max_length=7,
        choices=(
            ('Active', 'active'),
            ('Passive', 'passive'),
        ),
        default='passive',
        null=True,
    )
    cost_per_product = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cost per Product', )
    cost_per_delivery = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cost per Delivery', )
    fixed_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Fixed Cost', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', )

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(
            self.status,
            self.cost_per_product,
            self.cost_per_delivery,
            self.fixed_cost,
            self.created_at,
            self.updated_at,
        )

    class Meta:
        verbose_name = 'Delivery Cost'
        verbose_name_plural = 'Delivery Costs'
