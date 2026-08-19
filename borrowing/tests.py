from django.test import TestCase
from rest_framework.exceptions import ValidationError

from accounts.models import User
from books.models import Book, Author, Category
from borrowing.models import BorrowRecord
from borrowing.services import BorrowBook, ReturnBook


class BorrowBookTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="reza5",
            password="123456"
        )

        self.author = Author.objects.create(
            name="test author"
        )

        self.category = Category.objects.create(
            name="test category"
        )

        self.book = Book.objects.create(
            title="test book",
            author=self.author,
            category=self.category,
            isbn="TEST-001",
            total_copies=5,
            available_copies=5,
        )

    # -------------------------
    # Borrow Tests
    # -------------------------

    def test_borrow_book(self):
        borrow_record = BorrowBook().borrow(
            self.user,
            self.book,
            "2026-08-30"
        )

        self.book.refresh_from_db()

        self.assertEqual(
            self.book.available_copies,
            4
        )

        self.assertEqual(
            borrow_record.user,
            self.user
        )

        self.assertEqual(
            borrow_record.book,
            self.book
        )

        self.assertEqual(
            borrow_record.status,
            BorrowRecord.StatusChoices.BORROWED
        )

        self.assertEqual(
            BorrowRecord.objects.filter(
                user=self.user,
                book=self.book,
                status=BorrowRecord.StatusChoices.BORROWED
            ).count(),
            1
        )

    def test_user_cannot_borrow_more_than_three_books(self):
        books = []

        for i in range(4):
            book = Book.objects.create(
                title=f"Test Book {i}",
                author=self.author,
                category=self.category,
                isbn=f"TEST-{i}",
                total_copies=5,
                available_copies=5,
            )

            books.append(book)

        borrow_service = BorrowBook()

        borrow_service.borrow(
            self.user,
            books[0],
            "2026-08-30"
        )

        borrow_service.borrow(
            self.user,
            books[1],
            "2026-08-30"
        )

        borrow_service.borrow(
            self.user,
            books[2],
            "2026-08-30"
        )

        with self.assertRaises(ValidationError):
            borrow_service.borrow(
                self.user,
                books[3],
                "2026-08-30"
            )

        self.assertEqual(
            BorrowRecord.objects.filter(
                user=self.user,
                status=BorrowRecord.StatusChoices.BORROWED
            ).count(),
            3
        )

    def test_cannot_borrow_unavailable_book(self):
        self.book.available_copies = 0
        self.book.save()

        with self.assertRaises(ValidationError):
            BorrowBook().borrow(
                self.user,
                self.book,
                "2026-08-30"
            )

        self.book.refresh_from_db()

        self.assertEqual(
            self.book.available_copies,
            0
        )

        self.assertEqual(
            BorrowRecord.objects.filter(
                user=self.user,
                book=self.book
            ).count(),
            0
        )

    # -------------------------
    # Return Tests
    # -------------------------

    def test_return_book(self):
        borrow_record = BorrowBook().borrow(
            self.user,
            self.book,
            "2026-08-30"
        )

        self.book.refresh_from_db()

        self.assertEqual(
            self.book.available_copies,
            4
        )

        ReturnBook().return_borrowed_book(
            borrow_record
        )

        borrow_record.refresh_from_db()
        self.book.refresh_from_db()

        self.assertEqual(
            borrow_record.status,
            BorrowRecord.StatusChoices.RETURNED
        )

        self.assertIsNotNone(
            borrow_record.returned_at
        )

        self.assertEqual(
            self.book.available_copies,
            5
        )

    def test_cannot_return_book_twice(self):
        borrow_record = BorrowBook().borrow(
            self.user,
            self.book,
            "2026-08-30"
        )

        ReturnBook().return_borrowed_book(
            borrow_record
        )

        self.book.refresh_from_db()

        self.assertEqual(
            self.book.available_copies,
            5
        )

        with self.assertRaises(ValidationError):
            ReturnBook().return_borrowed_book(
                borrow_record
            )

        self.book.refresh_from_db()

        self.assertEqual(
            self.book.available_copies,
            5
        )

        borrow_record.refresh_from_db()

        self.assertEqual(
            borrow_record.status,
            BorrowRecord.StatusChoices.RETURNED
        )