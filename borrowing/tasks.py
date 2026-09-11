from django.core.mail import send_mail
from celery import shared_task


@shared_task
def test_task():
    return "celery is working"


@shared_task
def send_borrow_email(user_email, book_title):
    send_mail(
        subject="Book Borrowed Successfully",
        message=f"You successfully borrowed: {book_title}",
        from_email=None,
        recipient_list=[user_email],
    )
