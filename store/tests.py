from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
import uuid
from .models import Product

class ProductTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("99.99"),
            stock=10,
            description="Test description"
        )
        self.client = Client()

    def test_product_model(self):
        self.assertEqual(self.product.__str__(), "Test Product")
        self.assertTrue(isinstance(self.product.id, uuid.UUID))
        self.assertEqual(self.product.price, Decimal("99.99"))

    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('product_detail', args=[str(self.product.id)])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], self.product)

    def test_product_create(self):
        product_data = {
            'name': 'New Product',
            'price': '199.99',
            'stock': '20',
            'description': 'New product description'
        }
        response = self.client.post(reverse('product_new'), product_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 2)

    def test_search_results(self):
        response = self.client.get(reverse('search_results') + '?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
