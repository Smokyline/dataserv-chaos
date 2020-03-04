"""
WSGI config for chaos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chaos.settings")

application = get_wsgi_application()


try:
    activate_this = "/home/ivan/anaconda3/envs/swarm/bin/activate_this.py"
    exec(open(activate_this).read())
except Exception as e:
    print('no activate_this.py')