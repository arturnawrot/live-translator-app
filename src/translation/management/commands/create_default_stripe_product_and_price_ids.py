from django.core.management.base import BaseCommand
from django.conf import settings
import stripe
import os

class Command(BaseCommand):
    help = 'Create default Stripe product and price IDs'

    # Function to find existing product by metadata
    def find_existing_product(self, product_id):
        products = stripe.Product.list(limit=10)
        for product in products.auto_paging_iter():
            if product.metadata.get('id') == product_id:
                return product
        return None

    def find_existing_price(self, price_id, product_id):
        prices = stripe.Price.list(limit=10)
        for price in prices.auto_paging_iter():
            if price.metadata.get('id') == price_id and price.product == product_id:
                return price
        return None

    def handle(self, *args, **kwargs):
        product_id = settings.STRIPE_PRODUCT_ID
        price_id = settings.STRIPE_PRICE_ID

        product = self.find_existing_product(product_id)

        if not product:
            product = stripe.Product.create(
                name="Default subscription product",
                type="service",
                metadata={'id': product_id}
        )

        price = self.find_existing_price(price_id, product.id)

        if not price:
            price = stripe.Price.create(
                unit_amount=39900,
                currency='usd',
                recurring={'interval': 'month'},
                product=product.id,
                metadata={'id': price_id}
        )

        self.stdout.write(self.style.SUCCESS(f"Product ID: {product.id}"))
        self.stdout.write(self.style.SUCCESS(f"Price ID: {price.id}"))