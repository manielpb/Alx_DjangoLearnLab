from django.urls import path
from .views import (
    ListView,
    DeleteView,
    DetailView,
    UpdateView,
    CreateView
)

urlpatterns = [
    path("books/<int:pk>/", ListView.as_view(), name="book-list"),
    path("books/<int:pk>/", DetailView.as_view(), name="book-detail"),
    path("books/create/", CreateView.as_view(), name="books-create"),
    path("books/update", UpdateView.as_view(), name="book-update"),
    path("books/delete", DeleteView.as_view(), name = "book-delete")
]