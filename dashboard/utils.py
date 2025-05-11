from django.core.mail import send_mail
from django.conf import settings

def send_approval_email(user):
    subject = "Account Approved - You can now log in"
    message = f"Hello {user.name},\n\nYour account has been approved by admin. You can now log in using your email and password.\n\nLogin here: https://yourdomain.com/login/"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
