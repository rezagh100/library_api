from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import BorrowRecord


class BorrowBook:

    def book_limit(self, user):
        if user.borrow_records.filter(
            status=BorrowRecord.StatusChoices.BORROWED
        ).count() >= 3:
            raise ValidationError(
                "You cannot borrow more than 3 books at the same time."
            )

    def available_copies(self, book):
        if book.available_copies <= 0:
            raise ValidationError(
                "No available copies of the book."
            )

    def update_available_copies(self, book):
        book.available_copies -= 1
        book.save()

    def calculate_due_date(self):
        return timezone.now().date() + timezone.timedelta(
            days=settings.BORROW_DURATION_DAYS
        )

    def book_record(self, user, book, due_date):
        borrow_record = BorrowRecord.objects.create(
            user=user,
            book=book,
            due_date=due_date,
            status=BorrowRecord.StatusChoices.BORROWED,
        )
        return borrow_record

    def borrow(self, user, book, due_date=None):
        with transaction.atomic():
            self.book_limit(user)
            self.available_copies(book)
            self.update_available_copies(book)

            if due_date is None:
                due_date = self.calculate_due_date()

            return self.book_record(
                user,
                book,
                due_date
            )


class ReturnBook:

    def update_available_copies(self, book):
        book.available_copies += 1
        book.save()

    def return_book(self, borrow_record):
        borrow_record.status = BorrowRecord.StatusChoices.RETURNED
        borrow_record.returned_at = timezone.now()
        borrow_record.save()

    def return_borrowed_book(self, borrow_record):
        with transaction.atomic():
            if borrow_record.status != BorrowRecord.StatusChoices.BORROWED:
                raise ValidationError(
                    "This book has already been returned."
                )

            self.update_available_copies(
                borrow_record.book
            )

            self.return_book(
                borrow_record
            )
