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
def verify_acc_email(message, user_mail):

    send_mail(
        'Подтверждение регистрации',
        '',
        NAME_GMAIL,
        [user_mail],
        html_message=message,
        fail_silently=False
    )

    # email = EmailMessage(
    #     'Verify email',
    #     message,
    #     to=[user_mail],
    # )
    # email.send()



# def verify_acc_email(request, user):
#     current_site = get_current_site(request)
#
#     context = {
#         "domain": current_site.domain,
#         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#         "user": user,
#         "token": token_generator.make_token(user),
#     }
#
#     message = render_to_string(
#         'verify_email.html',
#         context=context,
#     )
#
#     email = EmailMessage(
#         'Verify email',
#         message,
#         to=[user.email],
#     )
#
#     email.send()