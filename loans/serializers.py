from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')
    member_username = serializers.ReadOnlyField(source='member.username')

    class Meta:
        model = Loan
        fields = ['id', 'member', 'member_username', 'book', 'book_title', 'borrow_date', 'return_date', 'status']