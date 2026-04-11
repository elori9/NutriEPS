from django.shortcuts import render
from .models import ConsumptionLog

# Create your views here.

def home(request):
    """Home page view - P6 logic. Now with mock data for P2 (Frontend)"""

    # NEED REAL DATA ....

    # Mock data following the contract so P2 can design the UI/charts
    context = {
        'calories_goal': 2000,
        'calories_consumed': 1450,
        'calories_remaining': 550,
        'todays_consumption_list': [
            {'food': {'name': 'Apple'}, 'quantity': 150},
        ]
    }
    return render(request, 'nutrieps/home.html', context)


def search(request):
    """Search page view - P4 logic. Now with mock data for P3 (Frontend)"""

    # NEED REAL DATA ....

    # Mock data following the contract so P2 can design the UI/charts
    context = {
        'search_term': "Chicken",
        'api_results': [
            {'name': 'Chicken Breast (Raw)', 'calories': 110, 'protein': 23, 'carbs': 0, 'fat': 1.2},
        ]
    }
    return render(request, 'nutrieps/search.html', context)


def profile(request):
    """Profile page view - P5 logic. Now with mock data for P3 (Frontend)"""

    # NEED REAL DATA ....

    # Mock data following the contract so P2 can design the UI/charts
    context = {
        'current_profile': {
            'weight': 72.5,
            'height': 180,
            'calories_goal': 2000
        }
        # The 'profile_form' will be sent by P5 when created, for now P3 can design it manually
    }
    return render(request, 'nutrieps/profile.html', context)


def history(request):
    """History page view - P6 logic. Now with mock data for P3 (Frontend)"""

    # NEED REAL DATA ....

    # Mock data following the contract so P2 can design the UI/charts
    context = {
        'historical_records': [
            {'date': '2026-04-10', 'food': {'name': 'Pizza'}, 'quantity': 300},
        ],
        'weight_history': [
            {'date': '2026-04-10', 'weight': 72.5},
        ]
    }
    return render(request, 'nutrieps/history.html', context)
