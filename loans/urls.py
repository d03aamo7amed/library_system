from django.urls import path
from .views import BorrowBookAPIView

urlpatterns = [
    path('api/borrow/<int:book_id>/', BorrowBookAPIView.as_view(), name='api_borrow_book'),
]