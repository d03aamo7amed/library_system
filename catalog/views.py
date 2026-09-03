from django.shortcuts import render
from django.db.models import Q, query
from rest_framework import generics, filters
from .models import Book
from .serializers import BookSerializer
from loans.models import Loan

def book_list_html(request):
    query = (request.GET.get('query') or request.GET.get('q') or request.GET.get('search') or '').strip()
    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    return render(request, 'catalog/book_list.html', {
        'books': books,
        'query': query,
    })


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'category']

def home(request):
    total_books = Book.objects.count()
    available_copies = sum(book.available_copies for book in Book.objects.all())
    active_loans = 0
    if request.user.is_authenticated:
        active_loans = Loan.objects.filter(member=request.user, return_date__isnull=True).count()

    recent_books = Book.objects.order_by('-id')[:3]

    context = {
        'total_books': total_books,
        'available_copies': available_copies,
        'active_loans': active_loans,
        'recent_books': recent_books,
    }
    return render(request, 'home.html', context)