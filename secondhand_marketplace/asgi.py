"""
ASGI config for secondhand_marketplace project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../apps'))

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secondhand_marketplace.settings')
application = get_asgi_application()

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secondhand_marketplace.settings')

application = get_asgi_application()
