import random
from django.core import mail

from heartUpBackend import settings
from . import models


def generate_otp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    return otp


def send_otp_email(email):
    subject = "One Time Password"
    otp_code = generate_otp()

    user = models.User.objects.get(email=email)
    current_site = "HeartUp.com"
    email_body = (f"Hi {user.first_name} thanks for singing up on {current_site}. "
                  f"Please verify your email with the \n one time passcode {otp_code}")
    from_email = settings.DEFAULT_FROM_EMAIL

    models.OneTimePassword.objects.create(user=user, code=otp_code)

    connection = mail.get_connection()
    connection.open()

    email_message = mail.EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    email_message.send(fail_silently=False)
    connection.close()


def send_normal_email(data):
    subject = data['email_subject']
    email_body = data['email_body']
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = data['to_email']

    connection = mail.get_connection()
    connection.open()

    email_message = mail.EmailMessage(
        subject=subject,
        body=email_body,
        from_email=from_email,
        # to=[to_email]
        to=["malikovnurbek186@gmail.com"]  # Remove this before production
    )
    email_message.send(fail_silently=False)
    connection.close()
