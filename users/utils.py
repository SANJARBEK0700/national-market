from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(user):
    subject = "Universal Market Verification Code"

    message = f"""
Salom {user.username},

Sizning tasdiqlash kodingiz:

{user.otp_code}

Kod 5 daqiqa amal qiladi.
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )