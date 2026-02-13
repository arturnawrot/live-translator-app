import stripe
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.models import User
class BaseStripeRepository:

    GLOBAL = 'global'

    CACHE_KEY = None
    CACHE_EXPIRATION_TIME = 3600

    def __init__(self, user=None):
        if user == None:
            user = self.GLOBAL

        self.user = user
        self.redis = cache

    def _get_cache_key(self):
        if self.CACHE_KEY == None:
            raise NotImplementedError()
        
        user_id = None

        if self.user == self.GLOBAL:
            user_id = self.GLOBAL
        elif isinstance(self.user, User):
            user_id = self.user.id
        else:
            raise Exception('Invalid user passed.')
        
        return f"user:{user_id}:{self.CACHE_KEY}"

    def __delete_from_cache(self):
        self.redis.delete(self._get_cache_key())

    def _get_from_stripe_api(self):
        raise NotImplementedError()
    
    def get(self, *args):
        cache_key = self._get_cache_key()
        
        cached_data = self.redis.get(cache_key)
        if cached_data is not None:
            return cached_data
        
        data = self._get_from_stripe_api(*args)
        self.redis.set(cache_key, data, self.CACHE_EXPIRATION_TIME)
        return data

    def refresh(self):
        self.__delete_from_cache()
        self.get()

class StripePaymentMethodRepository(BaseStripeRepository):
        
    CACHE_KEY = 'payment_methods'

    def _get_from_stripe_api(self):
        payment_methods = stripe.PaymentMethod.list(
            customer=self.user.payment_profile.get_stripe_id(),
            type='card'
        )
        self.__mark_default_method(payment_methods)
        return payment_methods

    def has_payment_method(self):
        payment_methods = self.get()
        return len(payment_methods.data) > 0
    
    def __mark_default_method(self, payment_methods):
        customer = self.user.payment_profile.get_stripe_customer()
        default_payment_method_id = customer.invoice_settings.default_payment_method

        for pm in payment_methods.data:
            pm.is_default = (pm.id == default_payment_method_id)

class StripeCustomerRepository(BaseStripeRepository):
    
    CACHE_KEY = 'customer'
    
    def _get_from_stripe_api(self):
        return stripe.Customer.retrieve(self.user.payment_profile.get_stripe_id())
    
class StripeDefaultSubscriptionPriceRepository(BaseStripeRepository):
    CACHE_KEY = 'subscription_price'

    def _get_from_stripe_api(self):
        # Retrieve all products (consider adding pagination handling if there are many products)
        products = stripe.Product.list(limit=1)  # Adjust limit as necessary
        product_id = None
        
        # Iterate through products to find the one with the matching metadata ID
        for product in products.auto_paging_iter():
            if product.metadata.get('id') == settings.STRIPE_PRODUCT_ID:
                product_id = product.id
                break

        if not product_id:
            return None

        # Retrieve all prices for the found product
        prices = stripe.Price.list(limit=10, product=product_id)  # Adjust limit as necessary

        # Iterate through prices to find the one with the matching metadata ID
        for price in prices.auto_paging_iter():
            if price.metadata.get('id') == settings.STRIPE_PRICE_ID:
                return price

        raise Exception('Default subscription price not found')
    
    def get_unit_amount(self):
        return self.get().unit_amount
    
    def get_price_id(self):
        return self.get().id
    
class StripeSubscriptionRepository(BaseStripeRepository):
    CACHE_KEY = 'user_subscriptions'

    def _get_from_stripe_api(self):
        # Retrieve all active subscriptions for the customer from Stripe
        return stripe.Subscription.list(
            customer=self.user.payment_profile.get_stripe_id(),
            status='active'
        )

    def is_subscribed_to_default(self):
        default_subscription_price_id = settings.STRIPE_PRICE_ID

        subscriptions = self.get()

        for subscription in subscriptions.auto_paging_iter():
            items = subscription['items'].data
            for item in items:
                if item['price']['metadata']['id'] == default_subscription_price_id:
                    return True

        return False