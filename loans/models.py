from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from catalog.models import Book

class Loan(models.Model):
    STATUS_CHOICES = (
        ('BORROWED', 'Borrowed'),
        ('RETURNED', 'Returned'),
    )

    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans', verbose_name="Member")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans', verbose_name="Book")
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name="Borrow Date")
    return_date = models.DateTimeField(null=True, blank=True, verbose_name="Return Date")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='BORROWED', verbose_name="Status")

    class Meta:
        ordering = ['-borrow_date']

    def clean(self):
        if not self.pk and self.book.available_copies <= 0:
            raise ValidationError(f"Cannot process loan: '{self.book.title}' has zero available copies!")
        
        if not self.pk:
            fourteen_days_ago = timezone.now() - timedelta(days=14)
            has_overdue = Loan.objects.filter(
                member=self.member, 
                status='BORROWED', 
                borrow_date__lt=fourteen_days_ago
            ).exists()
            
            if has_overdue:
                raise ValidationError(f"Cannot process loan: Member '{self.member.username}' has overdue books that must be returned first!")

    def __str__(self):
        return f"{self.member.username} borrowed {self.book.title}"