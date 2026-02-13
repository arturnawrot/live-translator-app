import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from translation.models import PaymentProfile
from translation.repositories import StripeDefaultSubscriptionPriceRepository

@csrf_exempt
def stripe_webhook_handler(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']
        stripe_customer_id = payment_method['customer']  # Assuming customer ID is stored as user ID

        PaymentProfile.objects.get(stripe_customer_id=stripe_customer_id).refresh_stripe_cache()

    if event['type'] in ['product.updated', 'price.updated', 'product.created', 'product.deleted', 'price.created', 'price.deleted']:
        StripeDefaultSubscriptionPriceRepository().refresh()

    return HttpResponse(status=200)