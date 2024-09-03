from django.core import mail

from heartUpBackend import settings


def send_normal_email(data):
    subject = data['email_subject']
    email_body = data['email_body']
    to_emails = data['to_email']
    from_email = settings.DEFAULT_FROM_EMAIL

    connection = mail.get_connection()
    connection.open()

    email_message = mail.EmailMessage(
        subject=subject,
        body=email_body,
        from_email=from_email,
        # to=to_emails
        to=['malikovnurbek186@gmail.com']   # Remove this before production
    )
    email_message.send(fail_silently=False)
    connection.close()
