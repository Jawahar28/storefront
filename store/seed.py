from store.models import Customer, Product, Collection, Order, OrderItem
from django.utils import timezone

def run():
    # Create a sample collection
    collection = Collection.objects.create(title="Electronics")

    # Create some products
    product1 = Product.objects.create(
        title="Smartphone",
        slug="smartphone",
        unit_price=699.99,
        inventory=50,
        collection=collection
    )

    product2 = Product.objects.create(
        title="Laptop",
        slug="laptop",
        unit_price=1200.00,
        inventory=30,
        collection=collection
    )

    # Create a customer
    customer = Customer.objects.create(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        membership="G"
    )

    # Create an order
    order = Order.objects.create(
        placed_at=timezone.now(),
        payment_status="P",
        customer=customer
    )

    # Add items to order
    OrderItem.objects.create(
        order=order,
        product=product1,
        quantity=2,
        unit_price=product1.unit_price
    )

    OrderItem.objects.create(
        order=order,
        product=product2,
        quantity=1,
        unit_price=product2.unit_price
    )

    print("✅ Database seeded successfully with sample data!")
