from django.apps import AppConfig
from django.conf import settings
import stripe
import os

class TranslationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translation'

    def ready(self):
        settings.FRONTEND_COMMUNICATION_PROTOCOL = os.getenv('FRONTEND_COMMUNICATION_PROTOCOL')
        
        settings.STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

        settings.STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
        
        stripe.api_key = settings.STRIPE_SECRET_KEY

        settings.STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

        settings.CRON_AUTH_TOKEN = os.getenv('CRON_AUTH_TOKEN')

        # Once the application is live, don't dare to change these 2 values
        settings.STRIPE_PRODUCT_ID = "default_subscription_product_id"
        settings.STRIPE_PRICE_ID = "default_subscription_price_id"
        
        import translation.signals
