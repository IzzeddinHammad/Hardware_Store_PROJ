from django.test import TestCase
from order.models import Order, OrderItem

class OrderModelsTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            token="testtoken",
            total=100.50,
            emailAddress="oleg5055355@gmail.com",
            billingName="Oleh Kravets",
            billingAddress1="1 Edenderry",
            billingCity="Edenderry",
            billingPostcode="12345",
            billingCountry="Ireland",
            shippingName="Oleh Kravets",
            shippingAddress1="1 Edenderry",
            shippingCity="Edenderry",
            shippingPostcode="12345",
            shippingCountry="Ireland",
            stripe_charge_id="stripe_12345",
            is_paid=True
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product="Hammer",
            price=25.99,
            quantity=2
        )

    def test_order_creation(self):
        self.assertEqual(self.order.token, "testtoken")
        self.assertEqual(self.order.emailAddress, "oleg5055355@gmail.com")
        self.assertEqual(self.order.billingName, "Oleh Kravets")
        self.assertTrue(self.order.is_paid)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.product, "Hammer")
        self.assertEqual(self.order_item.price, 25.99)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.sub_total(), 51.98)
