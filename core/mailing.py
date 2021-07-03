from django.core.mail import send_mail
from django.conf import settings

def send_ses_mail(subject, message, recepient):
    return send_mail(subject, message, f'"Pdpolls" <{settings.EMAIL_HOST_USER}>', [recepient], fail_silently = False)