from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from catalog.models import Book
from .models import Loan
from .serializers import LoanSerializer
from django.contrib import messages


# --- 1. HTML Views ---

@login_required
def borrow_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        
        if Loan.objects.filter(member=request.user, book=book, status='BORROWED').exists():
            messages.warning(request, f"أنت مستعير كتاب '{book.title}' بالفعل!")
        elif book.available_copies <= 0:
            messages.error(request, "عذراً، هذا الكتاب غير متاح حالياً.")
        else:
            Loan.objects.create(member=request.user, book=book)
            book.available_copies -= 1
            book.save()
            messages.success(request, f"تمت استعارة كتاب '{book.title}' بنجاح!")
            
            return redirect('loans:my_loans')

    return redirect('catalog:book_list')


@login_required
def my_loans(request):
    loans = Loan.objects.filter(
        member=request.user,
        status='BORROWED'
    )
    return render(request, 'loans/my_loans.html', {'loans': loans})


@login_required
def return_book(request, loan_id):
    if request.method == 'POST':
        loan = get_object_or_404(
            Loan,
            id=loan_id,
            member=request.user,
            status='BORROWED'
        )

        loan.status = 'RETURNED'
        loan.return_date = timezone.now()
        loan.save()

        loan.book.available_copies += 1
        loan.book.save()

    return redirect('loans:my_loans')


# --- 2. REST API Views ---

class BorrowBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Borrow a book",
        description="Creates a new loan for the authenticated user if book is available.",
        responses={201: LoanSerializer, 400: dict}
    )
    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Book not found.",
                "code": "NOT_FOUND"
            }, status=status.HTTP_404_NOT_FOUND)

        if book.available_copies <= 0:
            return Response({
                "status": "error",
                "message": f"Loan Failed: '{book.title}' has zero available copies in stock.",
                "code": "OUT_OF_STOCK"
            }, status=status.HTTP_400_BAD_REQUEST)

        if Loan.objects.filter(member=request.user, book=book, status='BORROWED').exists():
            return Response({
                "status": "error",
                "message": f"You already have an active loan for '{book.title}'.",
                "code": "ALREADY_BORROWED"
            }, status=status.HTTP_400_BAD_REQUEST)

        loan = Loan.objects.create(member=request.user, book=book)
        book.available_copies -= 1
        book.save()

        return Response({
            "status": "success",
            "message": f"Successfully borrowed '{book.title}'!",
            "data": LoanSerializer(loan).data
        }, status=status.HTTP_201_CREATED)