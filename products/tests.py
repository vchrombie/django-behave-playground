from rest_framework.test import APITestCase
from rest_framework import status

from .models import Category, Product


class CategoryTests(APITestCase):
    def test_create_category(self):
        data = {
            'title': 'test category',
            'parent_category_id': None
        }

        response = self.client.post('/products/category/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Category.objects.count(), 1)

        self.test_category = Category.objects.get()
        self.assertEqual(self.test_category.title, 'test category')
        self.assertEqual(
            str(self.test_category),
            "{} - {} - {} - {}".format(
                self.test_category.title,
                self.test_category.parent_category_id,
                self.test_category.created_at,
                self.test_category.updated_at
            )
        )

    def test_get_category(self):
        self.test_category1 = Category.objects.create(
            title='test category 1',
            parent_category_id=None
        )
        self.test_category2 = Category.objects.create(
            title='test category 2',
            parent_category_id=None
        )

        response = self.client.get("/products/category/{}/".format(self.test_category2.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.test_category2.id)

        response = self.client.get("/products/category/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)


class ProductTests(APITestCase):
    def test_create_product(self):
        self.test_category = Category.objects.create(
            title='test category',
            parent_category_id=None
        )
        data = {
            'category': self.test_category.id,
            'title': 'test product',
            'price': 100.00
        }
        response = self.client.post('/products/product/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Product.objects.count(), 1)

        self.test_product = Product.objects.get()
        self.assertEqual(self.test_product.title, 'test product')
        self.assertEqual(
            str(self.test_product),
            "{} - {} - {} - {} - {}".format(
                self.test_product.category,
                self.test_product.title,
                self.test_product.price,
                self.test_product.created_at,
                self.test_product.updated_at
            )
        )

    def test_get_product(self):
        self.test_category = Category.objects.create(
            title='test category',
            parent_category_id=None
        )
        self.test_product1 = Product.objects.create(
            category=self.test_category,
            title='test product 1',
            price=100.00
        )
        self.test_product2 = Product.objects.create(
            category=self.test_category,
            title='test product 2',
            price=200.00
        )

        response = self.client.get("/products/product/{}/".format(self.test_product2.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.test_product2.id)

        response = self.client.get("/products/product/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
