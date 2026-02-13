from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponsePermanentRedirect
from channels.middleware import BaseMiddleware
from translation.utils.stripe_utils import set_payment_method_as_default
from translation.models import ShareCode
from urllib.parse import urlparse, urlunparse

class RequirePaymentMethod:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_on_auth_page = 'auth' in request.path
        is_on_payment_setup_page = resolve(request.path_info).url_name == "setup-payment-method-page"
        is_logged_in = request.user.is_authenticated
        is_superuser = request.user.is_superuser
        is_on_app_page = 'app' in request.path

        if is_logged_in and not is_superuser and not is_on_payment_setup_page:
    
            if not request.user.payment_profile.has_payment_method() and (is_on_app_page or is_on_auth_page):
                return redirect(reverse('setup-payment-method-page'))
            
            if not request.user.payment_profile.is_subscription_active() and is_on_app_page:
                messages.error(request, "Please renew your subscription to continue using the app.")
                return redirect(reverse('dashboard'))

        response = self.get_response(request)

        return response
    
class ReloadCache:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.GET.get('reload_cache') == 'true' and request.user.is_authenticated:
            request.user.payment_profile.refresh_stripe_cache()

        response = self.get_response(request)

        return response

class AddAlert:
    def __init__(self, get_response):
        self.get_response = get_response

    def make_sure_payment_method_is_default_if_its_only_one(self, user):
        payment_methods = user.payment_profile.get()

        # If that's the only one payment method then make sure it's marked as default
        if len(payment_methods) == 1:
            if not payment_methods.data[0].is_default:
                set_payment_method_as_default(user.payment_profile.get_stripe_id(), payment_methods.data[0].id)
                
                user.payment_profile.refresh_stripe_cache()

    def __call__(self, request):
        if request.GET.get('stripe_payment_method_added'):
            self.make_sure_payment_method_is_default_if_its_only_one(request.user)
            messages.success(request, "Payment method added successfully")

        response = self.get_response(request)

        return response
    
class CustomAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Apply the standard authentication first
        await super().__call__(scope, receive, send)

        # If the user is anonymous, set to None
        if isinstance(scope['user'], AnonymousUser):
            scope['user'] = None

class ExcludeAuthenticatedUsersForGuestOnlyPages:
    EXCLUDED_VIEW_NAMES = [
        'login', 'register'
    ]

    REDIRECT_VIEW_NAME = 'dashboard'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if resolve(request.path_info).url_name in self.EXCLUDED_VIEW_NAMES:
                return redirect(reverse(self.REDIRECT_VIEW_NAME)) 

        response = self.get_response(request)

        return response
    
class SkipSubdomainWhenNecessary:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        parts = host.split('.')
        isSubdomainPassedInURL = len(parts) > 2 or (len(parts) > 1 and any(item in parts for item in ['localhost', '127.0.0.1']))
        isUserTryingToAccessOtherPageThanHero = resolve(request.path_info).url_name != 'hero'
        if isSubdomainPassedInURL and isUserTryingToAccessOtherPageThanHero:
            for part in parts:
                if ShareCode.objects.filter(code=part).exists():
                    new_url = request.build_absolute_uri().replace(part + '.', '')
                    print(new_url)
                    return HttpResponsePermanentRedirect(new_url)

        response = self.get_response(request)

        return response
