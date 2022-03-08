from rest_framework.test import APITestCase
from rest_framework import status

from .models import Campaign, Coupon
from products.models import Category, Product


class CategoryTests(APITestCase):
    def test_create_campaign(self):
        self.test_category = Category.objects.create(
            title='test category',
            parent_category_id=None
        )
        data = {
            'discount_type': 'Rate',
            'discount_rate': 10,
            'discount_amount': None,
            'min_purchased_items': 2,
            'apply_to': 'Category',
            'target_category': self.test_category.id,
            'test_product': None
        }

        response = self.client.post('/discounts/campaign/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Campaign.objects.count(), 1)

        self.test_campaign = Campaign.objects.get()
        self.assertEqual(self.test_campaign.discount_rate, 10)
        self.assertEqual(
            str(self.test_campaign),
            "{} - {} - {} - {} - {} - {} - {} - {} - {}".format(
                self.test_campaign.discount_type,
                self.test_campaign.discount_rate,
                self.test_campaign.discount_amount,
                self.test_campaign.min_purchased_items,
                self.test_campaign.apply_to,
                self.test_campaign.target_product,
                self.test_campaign.target_category,
                self.test_campaign.created_at,
                self.test_campaign.updated_at
            )
        )

    def test_get_campaign(self):
        self.test_category = Category.objects.create(
            title='test category',
            parent_category_id=None
        )
        self.test_product = Product.objects.create(
            category=self.test_category,
            title='test product',
            price=100.00
        )
        self.test_campaign = Campaign.objects.create(
            discount_type='Amount',
            discount_rate=None,
            discount_amount=10.00,
            min_purchased_items=2,
            apply_to='Product',
            target_product=self.test_product,
            target_category=None
        )

        response = self.client.get("/discounts/campaign/{}/".format(self.test_campaign.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.test_product.id)


class CouponTests(APITestCase):
    def test_create_coupon(self):
        data = {
            'discount_rate': 10,
            'min_cart_amount': 100.00
        }
        response = self.client.post('/discounts/coupon/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Coupon.objects.count(), 1)

        self.test_coupon = Coupon.objects.get()
        self.assertEqual(self.test_coupon.discount_rate, 10)
        self.assertEqual(
            str(self.test_coupon),
            "{} - {} - {} - {}".format(
                self.test_coupon.min_cart_amount,
                self.test_coupon.discount_rate,
                self.test_coupon.created_at,
                self.test_coupon.updated_at
            )
        )

    def test_get_coupon(self):
        self.test_coupon = Coupon.objects.create(
            discount_rate=10,
            min_cart_amount=100.00
        )

        response = self.client.get("/discounts/coupon/{}/".format(self.test_coupon.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.test_coupon.id)
