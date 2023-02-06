from celery import shared_task
from django.core.mail import send_mail
import os


@shared_task
def send_email(data):
    send_mail(
        subject=data['email_subject'],
        message=data['email_body'],
        from_email='ajaysoni.as812@gmail.com',
        recipient_list=[data['to_email']]
    )
    return True
