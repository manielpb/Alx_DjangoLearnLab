from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required



# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

#@login_required
#def admin_view(request):
    if request.user.userprofile.role != 'Admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    return HttpResponse("Welcome Admin! You have full access.")

def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse("Admin Dashboard")

@user_passes_test(is_librarian):
def librarian_view(request):
    return HttpResponse("Librarian Dashboard")

@user_passes_test(is_member)
def member_view(request):
    return HttpResponse("Member Dashboard")

@login_required
@user_passes_test(admin_view)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    pass

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    pass

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk)