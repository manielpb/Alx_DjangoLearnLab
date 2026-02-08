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
    path("books/<int:pk>/create/", CreateView.as_view(), name="books-create"),
    path("books/<int:pk>/update", UpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete", DeleteView.as_view(), name = "book-delete")
]