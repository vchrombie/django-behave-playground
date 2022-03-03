from .models import Campaign, Coupon


class AvailableDiscount:
    def __init__(self, discount_type, amount, min_purchased_items):
        self.discount_type = discount_type
        self.amount = amount
        self.min_purchased_items = min_purchased_items


class CampaignHelper:
    def __init__(self, cart_items):
        self.cart_items = cart_items
        self.available_discounts = []

    def get_campaign_discount(self):
        for cart_item in self.cart_items:
            self.get_product_discounts(cart_item)
            self.get_category_discounts(cart_item)

        return self.available_discounts

    def get_product_discounts(self, cart_item):
        campaigns = Campaign.objects.filter(
            apply_to='Product',
            target_product__in=[cart_item.item.id],
            min_purchased_items__lte=cart_item.quantity,
        )

        for campaign in campaigns:
            self.add_discount(campaign)

    def get_category_discounts(self, cart_item):
        campaigns = Campaign.objects.filter(
            apply_to='Category',
            target_product__in=[
                cart_item.item.category_id,
                cart_item.item.category.parent_category_id
            ],
            min_purchased_items__lte=cart_item.quantity,
        )

        for campaign in campaigns:
            self.add_discount(campaign)

    def add_discount(self, campaign):
        discount = AvailableDiscount(
            discount_type=campaign.discount_type,
            min_purchased_items=campaign.min_purchased_items,
            amount={
                'rate': campaign.discount_rate,
                'amount': campaign.discount_amount
            }
        )
        self.available_discounts.append(discount)


class CouponHelper:
    def __init__(self, cart_total_amount):
        self.cart_total_amount = cart_total_amount
        self.available_discounts = []

    def get_coupon_discount(self):
        coupon_discounts = Coupon.objects.filter(min_cart_amount__lte=self.cart_total_amount)

        for coupon_discount in coupon_discounts:
            discount = AvailableDiscount(
                discount_type='Rate',
                min_purchased_items=0,
                amount={
                    'rate': coupon_discount.discount_rate,
                    'amount': None
                }
            )
            self.available_discounts.append(discount)

        return self.available_discounts
