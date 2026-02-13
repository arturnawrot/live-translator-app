from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from translation.utils.stripe_utils import set_payment_method_as_default, renew_subscription as stripe_renew_subscription
from translation.repositories import StripeDefaultSubscriptionPriceRepository
from translation.models import Transaction
import stripe

# https://docs.stripe.com/payments/save-and-reuse?platform=web&ui=elements
@require_http_methods(["GET"])
def get_client_secret(request):
    if not request.user.is_authenticated:
      raise Exception('Not authenticated')

    if not hasattr(request.user, 'payment_profile'):
      raise Exception('User does not have any stripe ID')

    setupIntent = stripe.SetupIntent.create(
      customer=request.user.payment_profile.get_stripe_id(),
      automatic_payment_methods={"enabled": True},
    )

    if not setupIntent.client_secret:
      raise Exception('Client Secret not retrieved')

    return JsonResponse({
      'client_secret': setupIntent.client_secret
    })

@login_required
@csrf_protect
@require_http_methods(["POST"])
def delete_payment_method(request, payment_method_id):
    if len(request.user.payment_profile.get()) <= 1:
      messages.error(request, "You can't remove this payment method. You need to have a at least 1 active payment method. Add another one, then try removing this one.")
      return redirect('dashboard')

    try:
        stripe.PaymentMethod.detach(payment_method_id)
        request.user.payment_profile.refresh_stripe_cache()

        messages.success(request, "Payment Method removed")
    except stripe.error.StripeError as e:
        messages.error(request, "Something went wrong.")

    return redirect('dashboard')  

@login_required
@csrf_protect
@require_http_methods(["POST"])
def set_default_payment_method(request, payment_method_id: str):
    try:
      set_payment_method_as_default(request.user.payment_profile.get_stripe_id(), payment_method_id)
      
      request.user.payment_profile.refresh_stripe_cache()
              
      messages.success(request, "Payment Method Set as default")
    except:
      messages.error(request, "Something went wrong.")

    return redirect('dashboard')

@login_required
@csrf_protect
@require_http_methods(["POST"])
def renew_subscription(request):
    if request.user.payment_profile.is_subscription_active():
        messages.error(request, "You already have an active subscription.")
        return redirect('dashboard')
    
    if not request.user.payment_profile.has_payment_method():
        messages.error(request, "You need to have a payment method to renew your subscription.")
        return redirect('dashboard')
    
    try:
      subscription = stripe_renew_subscription(request.user)

      if subscription.status == 'incomplete':
        messages.error(request, "The transaction did not go through. Make sure your payment method is still valid.")
        return redirect('dashboard')

      messages.success(request, "Subscription created/renewed")
    except Exception as e:
      messages.error(request, "Something went wrong. Make sure your pement method is still valid.")

    request.user.payment_profile.refresh_stripe_cache()

    return redirect('dashboard')