from django.db import models

from products.models import Category, Product


class Campaign(models.Model):
    discount_type = models.CharField(
        max_length=6,
        choices=(
            ('Amount', 'amount'),
            ('Rate', 'rate'),
        ),
        default='rate',
        verbose_name='Discount Type',
    )
    discount_rate = models.IntegerField(null=True, blank=True, verbose_name='Discount Rate', )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, blank=True,
        verbose_name='Discount Amount',
    )
    min_purchased_items = models.IntegerField(verbose_name='Minimum Purchased Items', )
    apply_to = models.CharField(
        max_length=8,
        choices=(
            ('Product', 'product'),
            ('Category', 'category'),
        ),
        default='product',
        verbose_name='Applies to',
    )

    target_product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    target_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', )

    class Meta:
        verbose_name_plural = 'Campaigns'

    def __str__(self):
        return "{} - {} - {} - {} - {} - {} - {} - {} - {}".format(
            self.discount_type,
            self.discount_rate,
            self.discount_amount,
            self.min_purchased_items,
            self.apply_to,
            self.target_product,
            self.target_category,
            self.created_at,
            self.updated_at,
        )


class Coupon(models.Model):
    min_cart_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Minimum Cart Amount', )
    discount_rate = models.IntegerField(verbose_name='Discount Rate', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', )

    class Meta:
        verbose_name_plural = 'Coupons'

    def __str__(self):
        return "{} - {} - {} - {}".format(
            self.min_cart_amount,
            self.discount_rate,
            self.created_at,
            self.updated_at,
        )
