from rest_framework.test import APITestCase
from rest_framework import status

from .models import User, Cart, DeliveryCost
from products.models import Category, Product
from discounts.models import Campaign, Coupon


class UserTests(APITestCase):
    def test_create_user(self):
        data = {
            'username': 'admin',
            'password': 'admin'
        }

        response = self.client.post('/cart/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 1)

        self.test_user = User.objects.get()
        self.assertEqual(self.test_user.username, 'admin')
        self.assertEqual(
            str(self.test_user),
            "{}".format(
                self.test_user.username
            )
        )

    def test_get_user(self):
        self.test_user = User.objects.create(
            username='admin',
            password='admin'
        )

        response = self.client.get("/cart/user/{}/".format(self.test_user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.test_user.id)


class DeliveryCostTests(APITestCase):
    def test_create_delivery_cost(self):
        data = {
            'status': 'Active',
            'cost_per_delivery': 10.00,
            'cost_per_product': 5.00,
            'fixed_cost': 20.00
        }
        response = self.client.post('/cart/delivery-cost/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(DeliveryCost.objects.count(), 1)

        self.test_delivery_cost = DeliveryCost.objects.get()
        self.assertEqual(self.test_delivery_cost.fixed_cost, 20.00)
        self.assertEqual(
            str(self.test_delivery_cost),
            "{} - {} - {} - {} - {} - {}".format(
                self.test_delivery_cost.status,
                self.test_delivery_cost.cost_per_product,
                self.test_delivery_cost.cost_per_delivery,
                self.test_delivery_cost.fixed_cost,
                self.test_delivery_cost.created_at,
                self.test_delivery_cost.updated_at,
            )
        )

    def test_get_delivery_cost(self):
        self.test_delivery_cost = DeliveryCost.objects.create(
            status='Active',
            cost_per_delivery=10.00,
            cost_per_product=5.00,
            fixed_cost=20.00
        )

        response = self.client.get("/cart/delivery-cost/{}/".format(self.test_delivery_cost.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.test_delivery_cost.id)


class CartTests(APITestCase):
    def test_create_cart_item(self):
        self.test_user = User.objects.create(
            username='admin'
        )
        self.test_category = Category.objects.create(
            title='test category',
            parent_category_id=None
        )
        self.test_product = Product.objects.create(
            category=self.test_category,
            title='test product',
            price=10.00
        )
        data = {
            'user': self.test_user.id,
            'item': self.test_product.id,
            'quantity': 1
        }

        response = self.client.post('/cart/cart/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Cart.objects.count(), 1)

        self.test_cart = Cart.objects.get()
        self.assertEqual(self.test_cart.item.title, self.test_product.title)
        self.assertEqual(
            str(self.test_cart),
            "{} - {} - {} - {} - {}".format(
                self.test_cart.user,
                self.test_cart.item,
                self.test_cart.quantity,
                self.test_cart.created_at,
                self.test_cart.updated_at,
            )
        )

    def test_get_cart_item(self):
        self.test_user = User.objects.create(
            username='admin'
        )
        self.test_category = Category.objects.create(
            title='test category',
            parent_category_id=None
        )
        self.test_product = Product.objects.create(
            category=self.test_category,
            title='test product',
            price=10.00
        )
        self.test_cart = Cart.objects.create(
            user=self.test_user,
            item=self.test_product,
            quantity=1
        )

        response = self.client.get("/cart/cart/{}/".format(self.test_cart.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.test_cart.id)

    def test_checkout_by_user(self):
        self.test_user = User.objects.create(
            username='admin'
        )

        self.test_category1 = Category.objects.create(
            title='test category 1',
            parent_category_id=None
        )
        self.test_category2 = Category.objects.create(
            title='test category 2',
            parent_category_id=None
        )

        self.test_product1 = Product.objects.create(
            category=self.test_category1,
            title='test product 1',
            price=10.00
        )
        self.test_product2 = Product.objects.create(
            category=self.test_category2,
            title='test product 2',
            price=20.00
        )
        self.test_product3 = Product.objects.create(
            category=self.test_category2,
            title='test product 3',
            price=30.00
        )

        self.test_cart_item1 = Cart.objects.create(
            user=self.test_user,
            item=self.test_product1,
            quantity=1
        )
        self.test_cart_item2 = Cart.objects.create(
            user=self.test_user,
            item=self.test_product2,
            quantity=2
        )
        self.test_cart_item3 = Cart.objects.create(
            user=self.test_user,
            item=self.test_product3,
            quantity=3
        )

        self.test_delivery_cost = DeliveryCost.objects.create(
            status='Active',
            cost_per_delivery=10.00,
            cost_per_product=5.00,
            fixed_cost=20.00
        )

        self.test_campaign1 = Campaign.objects.create(
            discount_type='Amount',
            discount_rate=None,
            discount_amount=10.00,
            min_purchased_items=2,
            apply_to='Product',
            target_product=self.test_product3,
            target_category=None
        )
        self.test_campaign2 = Campaign.objects.create(
            discount_type='Rate',
            discount_rate=10,
            discount_amount=None,
            min_purchased_items=2,
            apply_to='Category',
            target_product=None,
            target_category=self.test_category2
        )
        self.test_campaign3 = Campaign.objects.create(
            discount_type='Rate',
            discount_rate=10,
            discount_amount=None,
            min_purchased_items=2,
            apply_to='Product',
            target_product=self.test_product3,
            target_category=None
        )

        self.test_coupon = Coupon.objects.create(
            discount_rate=10,
            min_cart_amount=100.00
        )

        response = self.client.get("/cart/cart/checkout/{0}/".format(self.test_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            len(response.data.get('checkout_details', False).get('products', False)),
            3
        )
        self.assertEqual(
            response.data.get('checkout_details', False).get('total', False)[0].get('total_price', False),
            140.00
        )
        self.assertEqual(
            response.data.get('checkout_details', False).get('total', False)[0].get('total_discount', False),
            28.00
        )
        self.assertEqual(
            response.data.get('checkout_details', False).get('amount', False)[0].get('total_amount', False),
            112.00
        )
        self.assertEqual(
            response.data.get('checkout_details', False).get('amount', False)[0].get('delivery_cost', False),
            55.00
        )

    def test_checkout_by_user_with_empty_cart(self):
        self.test_user = User.objects.create(
            username='admin'
        )
        self.test_delivery_cost = DeliveryCost.objects.create(
            status='Active',
            cost_per_delivery=10.00,
            cost_per_product=5.00,
            fixed_cost=20.00
        )

        response = self.client.get("/cart/cart/checkout/{0}/".format(self.test_user.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            response.data.get('checkout_details', False),
            False
        )
        self.assertEqual(
            response.data.get('Error', False),
            'Cart of the User is empty\n'
        )

    def test_checkout_by_user_with_no_delivery_cost(self):
        self.test_user = User.objects.create(
            username='admin'
        )
        self.test_category = Category.objects.create(
            title='test category',
            parent_category_id=None
        )
        self.test_product = Product.objects.create(
            category=self.test_category,
            title='test product',
            price=10.00
        )
        self.test_cart_item = Cart.objects.create(
            user=self.test_user,
            item=self.test_product,
            quantity=1
        )

        response = self.client.get("/cart/cart/checkout/{0}/".format(self.test_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data.get('checkout_details', False).get('amount', False)[0].get('delivery_cost', False),
            False
        )

    def test_checkout_by_user_with_no_user(self):
        self.test_category = Category.objects.create(
            title='test category',
            parent_category_id=None
        )
        self.test_product = Product.objects.create(
            category=self.test_category,
            title='test product',
            price=10.00
        )
        self.test_cart_item = Cart.objects.create(
            user=None,
            item=self.test_product,
            quantity=1
        )
        self.test_delivery_cost = DeliveryCost.objects.create(
            status='Active',
            cost_per_delivery=10.00,
            cost_per_product=5.00,
            fixed_cost=20.00
        )

        response = self.client.get("/cart/cart/checkout/{0}/".format(1))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            response.data.get('checkout_details', False),
            False
        )
        self.assertEqual(
            response.data.get('Error', False),
            'User not found. \nUser matching query does not exist.'
        )
