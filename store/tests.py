from django.test import TestCase
from django.utils import timezone
from accounts.models import User
from store.models import Order, OrderItem, Product, Category, Coupon
from customer.models import Address

class OrderModelTest(TestCase):
    def setUp(self):
        self.vendor = User.objects.create_user(username='vendoruser', email='vendor@example.com', password='vendorpass')
        self.customer = User.objects.create_user(username='customeruser', email='customer@example.com', password='customerpass')
        self.address = Address.objects.create(
            user=self.customer,
            full_name="John Doe",
            mobile="1234567890",
            email="john@example.com",
            country="Ireland",
            state="Leinster",
            city="Dublin",
            address="123 Main Street",
            zip_code="D01XY01"
        )
        self.category = Category.objects.create(title="Tools", slug="tools")
        self.product = Product.objects.create(
            name="Hammer",
            description="Steel hammer",
            category=self.category,
            price=10.00,
            regular_price=15.00,
            stock=100,
            shipping=5.00,
            status="Published",
            featured=True,
            vendor=self.vendor,
        )
        self.coupon = Coupon.objects.create(vendor=self.vendor, code="SAVE10", discount=10)
        self.order = Order.objects.create(
            customer=self.customer,
            sub_total=20.00,
            shipping=5.00,
            tax=2.00,
            service_fee=1.00,
            total=28.00,
            payment_status="Processing",
            payment_method="Stripe",
            order_status="Pending",
            initial_total=30.00,
            saved=2.00,
            address=self.address,
        )
        self.order.vendors.add(self.vendor)
        self.order.coupons.add(self.coupon)
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            qty=2,
            color="Red",
            size="M",
            price=10.00,
            sub_total=20.00,
            shipping=5.00,
            tax=2.00,
            total=28.00,
            initial_total=30.00,
            saved=2.00,
            vendor=self.vendor,
        )
        self.order_item.coupon.add(self.coupon)
        self.order_item.applied_coupon = True
        self.order_item.save()

    def test_order_creation(self):
        self.assertEqual(str(self.order), self.order.order_id)
        self.assertEqual(self.order.customer.username, "customeruser")
        self.assertEqual(self.order.total, 28.00)

    def test_order_vendors(self):
        self.assertIn(self.vendor, self.order.vendors.all())

    def test_order_coupons(self):
        self.assertIn(self.coupon, self.order.coupons.all())

    def test_order_address(self):
        self.assertEqual(self.order.address.full_name, "John Doe")

    def test_order_items_relation(self):
        self.assertIn(self.order_item, self.order.order_items())

    def test_order_item_creation(self):
        self.assertEqual(str(self.order_item), self.order_item.item_id)
        self.assertEqual(self.order_item.qty, 2)
        self.assertEqual(self.order_item.total, 28.00)

    def test_order_item_coupon(self):
        self.assertTrue(self.order_item.applied_coupon)
        self.assertIn(self.coupon, self.order_item.coupon.all())

    def test_order_item_vendor(self):
        self.assertEqual(self.order_item.vendor, self.vendor)

    def test_order_payment_status(self):
        self.assertEqual(self.order.payment_status, "Processing")

    def test_order_status_change(self):
        self.order.order_status = "Shipped"
        self.order.save()
        self.assertEqual(self.order.order_status, "Shipped")
