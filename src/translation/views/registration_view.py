from django.contrib.auth import login
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.db import transaction
from translation.forms import RegistrationForm
from translation.models import PaymentProfile
import stripe

class RegistrationView(FormView):
    template_name = 'auth/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('dashboard')

    @transaction.atomic
    def form_valid(self, form):
        user = form.save()
        stripe_customer_id = None
        try:
            customer = stripe.Customer.create(email=user.email)
            stripe_customer_id = customer['id']
            user.save()
            PaymentProfile(user=user, stripe_customer_id=stripe_customer_id).save()
            login(self.request, user)
        except Exception as e:
            if stripe_customer_id:
                try:
                    stripe.Customer.delete(stripe_customer_id)
                except Exception as delete_error:
                    print(f"Failed to delete Stripe customer: {delete_error}")
            raise e

        return super(RegistrationView, self).form_valid(form)