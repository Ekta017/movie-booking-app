from django.http import HttpResponse
from django.contrib.auth.models import User

def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@gmail.com", "admin123")
        return HttpResponse("Admin created successfully!")
    return HttpResponse("Admin already exists!")