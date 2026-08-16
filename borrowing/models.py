from django.db import models
from accounts.models import User
from books.models import Book


class BorrowRecord(models.Model):
    class StatusChoices(models.TextChoices):
        BORROWED = 'borrowed', 'Borrowed'
        RETURNED = 'returned', 'Returned'
        OVERDUE = 'overdue', 'Overdue'

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='borrow_records')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='borrow_records')
    borrowed_at = models.DateField(auto_now_add=True)
    returned_at = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.BORROWED
    )

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
