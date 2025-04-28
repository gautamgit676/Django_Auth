
import ssl
import time
import certifi
from time import sleep
from  celery import shared_task
from django.core.mail import send_mail
ssl_context = ssl.create_default_context(cafile=certifi.where())

@shared_task
def reg_send_emails(*userdata):
    subject = "User Authentication"
    message = f"Hello {userdata[1]}, You are Registered Successfully. Your OTP is {userdata[0]}"
    sender_email = 'gautamsinh987@gmail.com'
    recipient_list = [userdata[0]]

    send_mail (
                subject,
                message,
                sender_email,
                recipient_list,
                fail_silently=False,
                )
    
    send_mail(subject, message, sender_email, recipient_list)
    return 'Registration complited successfully'

@shared_task
def send_emails(*userdata):
    subject = "User Authentication"
    message = f"Hello {userdata[1]}, Your OTP is {userdata[0]}"
    sender_email = 'gautamsinh987@gmail.com'
    recipient_list = [userdata[2]]

    send_mail (
                subject,
                message,
                sender_email,
                recipient_list,
                fail_silently=False,
                )
    
    send_mail(subject, message, sender_email, recipient_list)
    return 'Email Send For OTP'