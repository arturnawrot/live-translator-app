from django.conf import settings
from translation.models import Usage, Transaction
from translation.repositories import StripeDefaultSubscriptionPriceRepository

def stripe_context(request):
    return {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY 
    }

def subscription_cost(request):
    return {
        'SUBSCRIPTION_COST': StripeDefaultSubscriptionPriceRepository().get_unit_amount()
    }

def user_stats(request):
    if not request.user.is_authenticated or request.user.is_superuser:
        return {}
    
    is_subscription_active = request.user.payment_profile.is_subscription_active()

    return {
        'total_unpaid_duration': request.user.profile.total_unpaid_duration,
        'total_amount_paid': Transaction.total_amount_paid(request.user),
        'is_subscription_active': is_subscription_active, 
        'is_subscription_active_read_friendly': "Active" if is_subscription_active else "Expired"
    }

def app_config(request):
    return {
        'FRONTEND_COMMUNICATION_PROTOCOL': settings.FRONTEND_COMMUNICATION_PROTOCOL
    }