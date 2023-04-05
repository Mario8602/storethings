from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator

from storething.celery import app
from storething.passwords import NAME_GMAIL
from .models import Order


@app.task()
def order_created(order_id, email_to, name_to):
    """Отправка уведомления о создании заказа на почту"""
    # order = Order.objects.get(id=order_id)
    subject = f'Заказ номер: {order_id}'
    message = f'Здравствуйте {name_to}, \n\n Ваш заказ успешно зарегистрирован. Ваш номер заказа: {order_id}'
    send_mail(
        subject,
        message,
        NAME_GMAIL,
        [email_to],
        fail_silently=False
    )


@app.task()
def verify_acc_email(domain, user_name, user_pk, user_mail):

    context = {
        "domain": domain,
        "uid": urlsafe_base64_encode(force_bytes(user_pk)),
        "user": user_name,
        "token": token_generator.make_token(user_name),
    }

    message = render_to_string(
        'verify_email.html',
        context=context,
    )

    email = EmailMessage(
        'Verify email',
        message,
        to=[user_mail],
    )

    email.send()