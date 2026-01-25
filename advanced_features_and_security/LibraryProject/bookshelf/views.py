from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

# Create your views here.
@permission_required('books.view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    render render(request, 'bookshelf/book_list.html', {'books': books})
