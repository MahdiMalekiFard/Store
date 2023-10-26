from django.db import models


class Category(models.Model):

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    class Meta:
        db_table = 'categories'


class Discount(models.Model):

    discount = models.CharField(max_length=255, blank=True)
    description = models.TextField()

    class Meta:
        db_table = 'discounts'


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    discounts = models.ManyToManyField(Discount, related_name='products', blank=True)

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.PositiveIntegerField(default=0)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'


class Comment(models.Model):

    COMMENT_STATUS_WAITING = 'W'
    COMMENT_STATUS_APPROVED = 'A'
    COMMENT_STATUS_UNAPPROVED = 'UA'

    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_UNAPPROVED, 'Un Approved'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    user = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'


class Customer(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    date_birth = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'customers'


class Address(models.Model):

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

    class Meta:
        db_table = 'address'


class Order(models.Model):

    ORDER_STATUS_PAID = 'P'
    ORDER_STATUS_UNPAID = 'U'
    ORDER_STATUS_CANCELED = 'C'

    ORDER_STATUS = [
        (ORDER_STATUS_PAID, 'Paid'),
        (ORDER_STATUS_UNPAID, 'Unpaid'),
        (ORDER_STATUS_CANCELED, 'Canceled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')

    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')

    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['order', 'product']]
        db_table = 'order_items'


class Cart(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carts'


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')

    quantity = models.SmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]
        db_table = 'cart_items'
