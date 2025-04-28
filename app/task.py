
import ssl
import time
import certifi
from time import sleep
from  celery import shared_task
from django.core.mail import send_mail
ssl_context = ssl.create_default_context(cafile=certifi.where())

@shared_task(bind=True, max_retries=3)
def reg_send_emails(self, *userdata):
    try:
        subject = "User Authentication"
        message = f"Hello {userdata[0]}, You are Registered Successfully"
        sender_email = 'gautamsinh987@gmail.com'
        reciver_email = userdata[1]
        recipient_list = (reciver_email,)
        send_mail (
                    subject,
                    message,
                    sender_email,
                    recipient_list,
                    fail_silently=False,
                    )
        
        send_mail(subject, message, sender_email, recipient_list)
        return 'Registration complited successfully'
    except Exception as e:
        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_emails(self, *userdata):
    try:
        subject = "OTP Verification"
        message = f"Hello {userdata[1]}, Your OTP is {userdata[0]} and valid for 5 minutes"
        sender_email = 'gautamsinh987@gmail.com'
        recipient_list = (userdata[2],)
        send_mail (
                    subject,
                    message,
                    sender_email,
                    recipient_list,
                    fail_silently=False,
                    )
        send_mail(subject, message, sender_email, recipient_list)
        return 'Email Send For OTP'
    except Exception as e:
        raise self.retry(exc=e, countdown=60)