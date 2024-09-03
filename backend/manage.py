#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.core.management import execute_from_command_line


def create_superuser():
    from django.contrib.auth import get_user_model
    User = get_user_model()

    admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL')
    admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
    admin_first_name = os.getenv('DJANGO_SUPERUSER_FIRST_NAME', 'Admin')
    admin_last_name = os.getenv('DJANGO_SUPERUSER_LAST_NAME', 'User')

    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(
            email=admin_email,
            password=admin_password,
            first_name=admin_first_name,
            last_name=admin_last_name
        )


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heartUpBackend.settings')
    try:
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

if __name__ == '__main__':
    main()
    if 'runserver' in sys.argv or 'migrate' in sys.argv:
        create_superuser()
