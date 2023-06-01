"""
ASGI config for a_ieum project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_ieum.settings')

# application = get_asgi_application()

# import os
# from django.core.asgi import get_asgi_application
# from daphne.server import Server

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_ieum.settings')
# django_asgi_app = get_asgi_application()
# server = Server(django_asgi_app, port_or_socket=8000)  # 포트 번호를 적절히 변경하세요.


# def run_daphne():
#     server.run()

# if __name__ == '__main__':
#     run_daphne()

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_ieum.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': URLRouter(websocket_urlpatterns),
    }
)