from django.shortcuts import render
from .models import ConsumptionLog

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
    model = ConsumptionLog  # Table where to query
    template_name = 'nutrieps/history.html'
    context_object_name = 'logs'  # variable name in template
