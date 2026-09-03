from django.urls import path
from .views import BookListView, book_list_html
from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.book_list_html, name='book_list'),
    path('api/books/', BookListView.as_view(), name='api_books'),

]