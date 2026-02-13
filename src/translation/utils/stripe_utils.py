import stripe
from translation.models import PaymentProfile, Transaction, Usage, HourlyPricing
from translation.exceptions import MinimumChargeError
from translation.repositories import StripeDefaultSubscriptionPriceRepository

def set_payment_method_as_default(customer_id: str, payment_method_id: str):
    stripe.Customer.modify(
        customer_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        }
    )

def charge_user_for_unpaid_usage(user, is_on_delete=False):
    payment_profile = PaymentProfile.objects.get(user=user)

    if not payment_profile.has_payment_method():
        raise ValueError("No payment method available")

    total_unpaid_duration = user.profile.total_unpaid_duration

    # (X seconds / 60 seconds ) * $rate_per_minute
    amount_to_charge = user.payment_profile.amount_to_charge

    # Stripe requires at least 50 cents to be charged
    if total_unpaid_duration > 0 and is_on_delete and amount_to_charge < 0.50:
        amount_to_charge = 0.50

    if amount_to_charge < 0.50:
        raise MinimumChargeError('The user needs to own at least $0.50 otherwise Stripe will not process the charge.')

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount_to_charge * 100),  # Convert dollars to cents
            currency="usd",
            customer=payment_profile.get_stripe_id(),
            description=f"Charge for {total_unpaid_duration} seconds of usage",
            payment_method=payment_profile.get_default_stripe_payment_method_id(),
            confirm=True,
            off_session=True
        )

        transaction = Transaction.objects.create(
            user=user,
            stripe_charge_id=payment_intent.id,
            amount=amount_to_charge,
            was_successful=(payment_intent.status == 'succeeded')
        )

        unpaid_usages = Usage.get_unpaid_usages(user=user)
        transaction.related_usages.set(unpaid_usages)
        unpaid_usages.update(payment_status='paid')

        payment_profile.refresh_stripe_cache()
        return payment_intent
    except stripe.error.StripeError as e:
        raise e
    
def renew_subscription(user, create_transaction=True):
    user_stripe_id = user.payment_profile.get_stripe_id()

    subscription = stripe.Subscription.create(
        customer=user_stripe_id,
        items=[
            {
                'price': StripeDefaultSubscriptionPriceRepository().get_price_id(),
            },
        ],
        metadata={'app_user_id': user.id},
      )

    subscription_price = subscription['items']['data'][0]['price']['unit_amount'] / 100

    if create_transaction:
        Transaction.objects.create(
            user=user,
            stripe_charge_id=subscription.latest_invoice,
            amount=subscription_price,
            was_successful=(subscription.status == 'active')
        )

    return subscription