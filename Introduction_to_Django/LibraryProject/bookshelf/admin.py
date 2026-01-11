from django.contrib import admin
from .models import Book

# Use @admin.register to satisfy "register"
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):  # Must inherit admin.ModelAdmin
    # Columns to display
    list_display = ('title', 'author', 'publication_year')

    # Filters on the sidebar
    list_filter = ('author', 'publication_year')

    # Search bar
    search_fields = ('title', 'author')
