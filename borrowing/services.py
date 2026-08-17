from django.core.exceptions import ValidationError
from .models import BorrowRecord


class BorrowBook:

    def book_limit(self, user):
        if user.borrow_records.filter(
            status=BorrowRecord.StatusChoices.BORROWED).count() >= 3:
            raise ValidationError("You cannot borrow more than 3 books at the same time.")

    def available_copies(self, book):
        if book.available_copies <= 0:
            raise ValidationError("No available copies of the book.")

    def update_available_copies(self, book):
        book.available_copies -= 1
        book.save()

    def book_record(self, user, book, due_date):
        borrow_record = BorrowRecord.objects.create(
            user=user,
            book=book,
            due_date=due_date,
            status=BorrowRecord.StatusChoices.BORROWED,
        )
        return borrow_record

    def borrow(self, user, book, due_date):
        self.book_limit(user)
        self.available_copies(book)
        self.update_available_copies(book)

        borrow_record = self.book_record(
            user,
            book,
            due_date
        )

        return borrow_record
