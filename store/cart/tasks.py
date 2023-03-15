from django.core.mail import send_mail
from storething.celery import app


# @shared_task()
# def order_created(a, b):
#     """Отправка уведомления о создании заказа на почту"""
    # order = Order.objects.get(id=order_id)
    # subject = f'Заказ номер: {order_id}'
    # message = f'Здравствуйте {order_id}, \n\n Ваш заказ успешно зарегистрирован. Ваш номер заказа: {order_id}'
    # return send_mail(
    #     subject,
    #     message,
    #     'hellp8901@gmail.com',
    #     ['hellp8901@yandex.ru'],
    #     fail_silently=False
    # ) # admin@storethings.com


@app.task()
def send_task(order_id):
    send_mail(
        'Вы подписались',
        f'Ваш заказ номер {order_id} оформлен',
        'Hellp8901@gmail.com',
        ['Hellp8901@yandex.ru'],
        fail_silently=False,
    )