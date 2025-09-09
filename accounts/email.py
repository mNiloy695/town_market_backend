from django.conf import settings
from django.core.mail import send_mail
import threading
def send_email(subject,message,receiver_email):

    threading.Thread(
        target=send_mail,
        args=(subject, message, settings.EMAIL_HOST_USER,[receiver_email])
    ).start()
