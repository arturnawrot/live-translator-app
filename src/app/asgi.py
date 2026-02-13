"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

import django

django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

# @TODO Resolve websocket_urlpatterns from each app automatically without having have to manually import them.
from app.urls import websocket_urlpatterns as app_websocket_urlpatterns
from translation.urls import websocket_urlpatterns as translation_websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from translation.middlewares import CustomAuthMiddleware

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "https": django_asgi_app,

    "websocket": AuthMiddlewareStack(
        CustomAuthMiddleware(
            URLRouter(
                app_websocket_urlpatterns +
                translation_websocket_urlpatterns
            )
        )
    )
})