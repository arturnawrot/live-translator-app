from django.db import models
from django.contrib.auth.models import User
from translation.repositories import StripePaymentMethodRepository, StripeCustomerRepository, StripeSubscriptionRepository
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    @property
    def total_unpaid_duration(self):
        return Usage.total_unpaid_duration(self.user)

class PaymentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payment_profile')
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)

    @property
    def amount_to_charge(self):
        return round((self.user.profile.total_unpaid_duration / 60) * (HourlyPricing.objects.latest('id').price / 100), 2)
    
    @property
    def stripe_payment_method_repository(self) -> StripePaymentMethodRepository:
        return StripePaymentMethodRepository(self.user)
    
    @property
    def stripe_customer_repository(self) -> StripeCustomerRepository:
        return StripeCustomerRepository(self.user)
    
    @property
    def stripe_subscription_repository(self) -> StripeSubscriptionRepository:
        return StripeSubscriptionRepository(self.user)

    def get_stripe_id(self) -> str:
        return self.stripe_customer_id
    
    def has_payment_method(self) -> bool:
        return self.stripe_payment_method_repository.has_payment_method()
    
    def get(self) -> bool:
        return self.stripe_payment_method_repository.get()
    
    def get_stripe_customer(self):
        return self.stripe_customer_repository.get()
    
    def get_default_stripe_payment_method_id(self):
        payment_methods = self.get()
        for payment_method in payment_methods:
            if payment_method.is_default:
                return payment_method.id
        return None
    
    def is_subscription_active(self):
        return self.stripe_subscription_repository.is_subscribed_to_default()
    
    def refresh_stripe_cache(self):
        self.stripe_customer_repository.refresh()
        self.stripe_payment_method_repository.refresh()
        self.stripe_subscription_repository.refresh()

class Usage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usage')
    duration = models.FloatField(help_text="Duration in seconds")
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, default='unpaid', help_text="Payment status: unpaid, pending, paid")

    @classmethod
    def get_unpaid_usages(cls, user=None):
        query = cls.objects.filter(payment_status='unpaid')
        if user:
            query = query.filter(user=user)
        return query
    
    @classmethod
    def total_unpaid_duration(cls, user):
        unpaid_usages = cls.get_unpaid_usages(user=user)
        total_duration = unpaid_usages.aggregate(total_duration=models.Sum('duration')).get('total_duration', 0)
        if total_duration is None:
            return 0
        return round(total_duration, 2)

    def __str__(self):
        return f"{self.user.username} - {self.duration} seconds on {self.date}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    stripe_charge_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    was_successful = models.BooleanField(default=False)
    related_usages = models.ManyToManyField(Usage, related_name='transactions')

    @classmethod
    def total_amount_paid(cls, user):
        total_paid = cls.objects.filter(user=user, was_successful=True)\
                                .aggregate(total_paid=models.Sum('amount'))\
                                .get('total_paid', 0)
        
        return 0 if total_paid == None else round(total_paid, 2)

    def __str__(self):
        return f"Transaction {self.id}: {self.amount} (Successful: {self.was_successful})"
    
class ShareCode(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='share_code' 
    )
    code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s share code"
    
class HourlyPricing(models.Model):
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"Hourly Pricing: ${self.price}"
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    company_name = models.CharField(max_length=255)
    company_size = models.CharField(max_length=6, choices=[
        ('small', 'Small (1-50 employees)'),
        ('medium', 'Medium (51-250 employees)'),
        ('large', 'Large (251+ employees)')
    ])
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} from {self.company_name}"
    
class TranscriptRecord(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=True, null=True, blank=True)
    
    datetime = models.DateTimeField()

    content = models.TextField()

    def __str__(self):
        return f"Record {self.uuid} from {self.datetime}: '{self.content}'"