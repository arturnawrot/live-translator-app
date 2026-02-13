# translation/urls.py
from django.urls import path

from translation.views.views import contact, hero, index, translate, index_with_share_code
from translation.views.stripe_views import get_client_secret, delete_payment_method, set_default_payment_method, renew_subscription
from translation.views.auth_views import dashboard_page, setup_payment_method_page, logout, charge_yourself, list_transactions
from translation.consumers.translation_consumer import TranslationConsumer
from translation.views.registration_view import RegistrationView
from translation.views.stripe_webhook_handler import stripe_webhook_handler
from translation.views.login_view import LoginView
from translation.views.cron_views import handle_cron
from translation.views.share_code_view import ShareCodeView, DeleteShareCodeView
from translation.views.user_delete_view import UserDeleteView
from translation.views.contact_view import ContactView

urlpatterns = [  
    path('translate', translate),
    path('auth/home', dashboard_page, name='dashboard'),

    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),

    path('auth/delete-payment-method/<str:payment_method_id>/', delete_payment_method, name='delete-payment-method'),
    path('auth/setupPaymentMethod/', setup_payment_method_page, name='setup-payment-method-page'),
    path('api/getClientSecret', get_client_secret, name='get-client-secret'),
    path('auth/submitPaymentMethod', translate, name='submit-payment-method'),
    path('auth/set-default-payment-method/<str:payment_method_id>/', set_default_payment_method, name='set-default-payment-method'),
    path('auth/share-code/', ShareCodeView.as_view(), name='share-code-page'),
    path('auth/delete-share-code/', DeleteShareCodeView.as_view(), name='delete-share-code'),
    path('auth/delete-account/<int:pk>/', UserDeleteView.as_view(), name='delete-account'),
    path('auth/charge', charge_yourself, name='charge'),
    path('auth/renew-subscription', renew_subscription, name='renew-subscription'),
    path('auth/transactions', list_transactions, name='list_transactions'),

    path('share/<str:code>/', index_with_share_code, name='share-code-view'),

    path('stripe_webhooks', stripe_webhook_handler, name='stripe_webhooks'),
    path('cron', handle_cron, name='cron'),

    path('app/', index, name='index'),
    path('contact/', ContactView.as_view(), name='contact'),


    path('', hero, name='hero')
]

websocket_urlpatterns = [
    path("translate", TranslationConsumer.as_asgi())
]