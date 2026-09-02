from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from catalog.models import Book
from .models import Loan
from .serializers import LoanSerializer

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