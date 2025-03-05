from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from order.models import Order, OrderItem
from store.models import Product, Category
from django.contrib.auth import get_user_model

class OrderModelsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@t.com',
            password='tpassword'
        )
        self.category = Category.objects.create(name="Tools")
        self.product = Product.objects.create(
            name="Hammer",
            category=self.category,
            price=25.99,
            stock=50,
            available=True
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name="Oleh Kravets",
            address="1 Edenderry",
            city="Edenderry",
            created_at=timezone.now(),
            updated_at=timezone.now(),
            paid=True
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=2
        )

    def test_order_creation(self):
        self.assertEqual(self.order.full_name, "Oleh Kravets")
        self.assertEqual(self.order.city, "Edenderry")
        self.assertTrue(self.order.paid)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.price, 25.99)
        self.assertEqual(self.order_item.quantity, 2)

class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(name="Tools")
        self.product = Product.objects.create(
            name="Hammer",
            category=self.category,
            price=25.99,
            stock=50,
            available=True
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name="Oleh Kravets",
            address="1 Edenderry",
            city="Edenderry",
            paid=True
        )

    def test_order_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('order:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order_list.html')

    def test_order_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('order:order_detail', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Oleh Kravets')
        self.assertTemplateUsed(response, 'order/order_detail.html')

class OrderUrlsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name="Oleh Kravets",
            address="1 Edenderry",
            city="Edenderry",
            paid=True
        )

    def test_order_list_url(self):
        url = reverse('order:order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_order_detail_url(self):
        url = reverse('order:order_detail', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
