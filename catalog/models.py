from django.db import models
from django.core.exceptions import ValidationError

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    author = models.CharField(max_length=100, verbose_name="Author")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    category = models.CharField(max_length=50, verbose_name="Category")
    total_copies = models.PositiveIntegerField(default=1, verbose_name="Total Copies")
    available_copies = models.PositiveIntegerField(default=1, verbose_name="Available Copies")
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name="Book Cover")
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name="Book Cover Image")
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']

    def clean(self):
        if self.available_copies > self.total_copies:
            raise ValidationError({'available_copies': 'Available copies cannot be greater than total copies!'})

    def __str__(self):
        return f"{self.title} - {self.author}"