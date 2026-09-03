from django.urls import path
from .views import BorrowBookAPIView, my_loans, return_book
from . import views

app_name = 'loans'
urlpatterns = [
    path('api/borrow/<int:book_id>/', BorrowBookAPIView.as_view(), name='api_borrow_book'),
    path('my-loans/', my_loans, name='my_loans'),
    path('return/<int:loan_id>/', return_book, name='return_book'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
]