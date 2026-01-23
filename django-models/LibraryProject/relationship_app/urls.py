from django.urls import path, include
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import admin_view, librarian_view, member_view

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('login/',LoginView.as_view(template_name='relationship_app/'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/'), name='logout'),
   app.urls')),
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    path('books/add_book/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit_book', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete', views.delete_book, name='delete_book'),
]   