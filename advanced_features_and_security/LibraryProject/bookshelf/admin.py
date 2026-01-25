from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin

# Use @admin.register to satisfy "register"
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):  # Must inherit admin.ModelAdmin
    # Columns to display
    list_display = ('title', 'author', 'published_year')

    # Filters on the sidebar
    list_filter = ('author', 'published_year')

    # Search bar
    search_fields = ('title', 'author')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_active")

    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    search_fields = ("username", "email")

    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        ("Profile Info", {"fields": ("date_of_birth", "profile_photo")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
    (
        "Profile Info", {"fields": ("date_of_birth", "profile_photo")}
    ),
    )

admin.site.register(CustomUser, CustomUserAdmin)