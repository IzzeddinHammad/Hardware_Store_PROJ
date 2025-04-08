from django.test import TestCase , Client
from cart.models import Cart , CartItem
from store.models import Product
from accounts.models import vendor
from django.contrib.auth import get_user_model



User = get_user_model()

# Create your tests here.

# testing the model
class CartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.product = Product.objects.create(
            name = 'Test Product',
            price = 10.00,
            stock = 10
        )

        self.cart = Cart.objects.create(cart_id = 'test_cart_id')
        self.cart_item = CartItem.objects.create(
            product = self.product,
            cart = self.cart,
            quantity = 2
        )


    def test_cart_creation(self):
        self.assertEqual(str(self.cart) , 'test_cart_id')
        self.assertTrue(hasattr(self.cart , 'date_added'))

    def test_cart_item_creation(self):
        self.assertEqual(str(self.cart_item.product) , 'Test Product')
        self.assertEqual(self.cart_item.sub_total(), 20.00)
        self.assertTrue(self.cart_item.active)


