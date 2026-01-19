from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_authenticated and u.userprofile.role == 'Admin')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')
