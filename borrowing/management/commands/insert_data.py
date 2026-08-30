from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from books.models import Author, Book, Category
from borrowing.services import BorrowBook


class Command(BaseCommand):
    help = "Create 100 borrow records for testing and demo data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of borrow records to create. Defaults to 100.",
        )

    def handle(self, *args, **options):
        count = options["count"]

        if count < 1:
            self.stdout.write(
                self.style.WARNING("The count must be at least 1.")
            )
            return

        author, _ = Author.objects.get_or_create(name="Sample Author")
        category, _ = Category.objects.get_or_create(name="Sample Category")
        borrow_service = BorrowBook()

        for index in range(1, count + 1):
            username = f"member-{index}"
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "password": "pbkdf2_sha256$600000$dummy$dummy",
                    "role": User.Role.MEMBER,
                },
            )

            isbn = f"978-1-{index:05d}"
            book, _ = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "title": f"Sample Book {index}",
                    "author": author,
                    "category": category,
                    "total_copies": 5,
                    "available_copies": 5,
                },
            )

            due_date = timezone.now().date() + timezone.timedelta(days=14)
            borrow_service.borrow(user, book, due_date)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} borrow records.")
        )
