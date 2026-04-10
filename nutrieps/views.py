from django.shortcuts import render

# Create your views here.

def home(request):
    """Home page view."""
    return render(request, 'nutrieps/home.html')

def search(request):
    """Search page view."""
    return render(request, 'nutrieps/search.html')

def profile(request):
    """Profile page view."""
    return render(request, 'nutrieps/profile.html')

def history(request):
    """History page view."""
    return render(request, 'nutrieps/history.html')
