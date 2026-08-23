from django.core.management.base import BaseCommand
from django.utils import timezone

from borrowing.models import BorrowRecord


class Command(BaseCommand):

    def handle(self, *args, **options):

        today = timezone.now().date()
        

        records = BorrowRecord.objects.filter(
            status=BorrowRecord.StatusChoices.BORROWED,
            due_date__lt=today
        )

        for record in records:
            record.status = BorrowRecord.StatusChoices.OVERDUE
            record.save()
        self.stdout.write(
            self.style.SUCCESS(
                "Overdue records updated successfully."
            )
        )