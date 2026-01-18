author_name = "George Orwell"
orwell_books = Book.objects.filter(author__name=author_name)
print(f"books by {author_name}:")
for book in orwell_books:
    print(f"- {book.title}")
