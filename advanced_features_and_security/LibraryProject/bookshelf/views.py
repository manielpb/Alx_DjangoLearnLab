from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookSearchForm, ExampleForm
from django.db.models import Q

# Create your views here.
@permission_required('books.view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def book_list(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q: 
            books = books.filter(
                Q(title__icontains=q) | Q(author__icontains=q)
            )
    return render(request, "bookshelf/book_list.html", {"form": form, "books": books})