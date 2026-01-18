from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})