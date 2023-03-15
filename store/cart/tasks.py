from django.core.mail import send_mail
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


# @app.task()
# def send_task(order_id):
#     send_mail(
#         'Вы подписались',
#         f'Ваш заказ номер {order_id} оформлен',
#         'gmail.com',
#         ['yandex.ru'],
#         fail_silently=False,
#     )