from django.db import models

# Create your models here.

class Author(models.model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)

class Library(models.model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)

class Librarian(models.model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(Library)