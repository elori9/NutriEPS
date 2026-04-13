from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .form import UserProfileForm
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


@login_required
def profile(request):
    """Profile page view - P5 logic. Handles BMR calculation and profile updates."""
    calculated_calories = None
    weight = None
    height = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            activity_level = float(form.cleaned_data['activity_level'])

            # 2. Perform calculations (Mifflin-St Jeor formula)
            if gender == 'M':
                tmb = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                tmb = (10 * weight) + (6.25 * height) - (5 * age) - 161

            calculated_calories = round(tmb * activity_level)

            # 3. Save to Database
            # PENDING: Replace "UserProfile" and "user_profile" with the real model
            # when the database teammate provides the exact names.
            # user_profile = request.user.userprofile
            # user_profile.weight = weight
            # user_profile.height = height
            # user_profile.daily_goal = calculated_calories
            # user_profile.save()

    else:
        # 1. If the user is just visiting the page (GET request)
        form = UserProfileForm()

        # PENDING: Read real data from the DB if the user already has a profile
        # if hasattr(request.user, 'userprofile'):
        #     weight = request.user.userprofile.weight
        #     height = request.user.userprofile.height
        #     calculated_calories = request.user.userprofile.daily_goal

        # Meanwhile, use mock data if nothing is calculated yet
        weight = 72.5
        height = 180
        calculated_calories = 2000

    # 4. Context dictionary to send to the Frontend (P3)
    # The 'profile_form' is now real and ready for P3 to render.
    context = {
        'profile_form': form,
        'current_profile': {
            'weight': weight,
            'height': height,
            'calories_goal': calculated_calories
        }
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


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
