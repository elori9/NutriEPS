from os import name

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserProfileForm, ConsumptionForm
from .models import UserProfile, ConsumptionLog, WeightLog, FoodItem

from .services import search_foods


# Create your views here.

def home(request):
    """Home page view - P6 logic. Real data from database"""
    from django.utils import timezone

    # Si l'usuari no ha iniciat sessió, enviem-lo a l'HTML perquè vegi el Landing Page
    if not request.user.is_authenticated:
        return render(request, 'nutrieps/home.html', {})

    today = timezone.now().date()

    # 1. Obtenir les metes de l'usuari (P5)
    user_goal = 2000  # Valor per defecte
    if hasattr(request.user, 'userprofile') and request.user.userprofile.calories_goal:
        user_goal = request.user.userprofile.calories_goal

    # 2. Obtenir els registres d'avui de la base de dades
    logs = ConsumptionLog.objects.filter(user=request.user, date=today)

    # 3. Sumar calories i macros
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    todays_list = []

    for log in logs:
        # Assumim que la informació de l'aliment a FoodItem està en format "per 100 grams"
        factor = log.quantity / 100.0

        cals = log.food.calories * factor
        prot = log.food.protein * factor
        carbs = log.food.carbs * factor
        fat = log.food.fat * factor

        total_calories += cals
        total_protein += prot
        total_carbs += carbs
        total_fat += fat

        todays_list.append({
            'food': {'name': log.food.name},
            'quantity': log.quantity,
            'calories': round(cals, 1)
        })

    calories_remaining = user_goal - total_calories
    if calories_remaining < 0:
        calories_remaining = 0

    # Mock data following the contract so P2 can design the UI/charts
    context = {
        'calories_goal': round(user_goal),
        'calories_consumed': round(total_calories),
        'calories_remaining': round(calories_remaining),
        'total_protein': round(total_protein, 1),
        'total_carbs': round(total_carbs, 1),
        'total_fat': round(total_fat, 1),
        'todays_consumption_list': todays_list
    }
    return render(request, 'nutrieps/home.html', context)


def search(request):
    """Search page view - P4 logic with real API data."""

    search_term = request.GET.get("q", "").strip()
    api_results = []
    error_message = None

    if search_term:
        local_food = FoodItem.objects.filter(name__icontains=search_term)
        if local_food.exists():
            for food in local_food:
                api_results.append({
                    'name':food.name,
                    'calories':food.calories,
                    'protein': food.protein,
                    'carbs': food.carbs,
                    'fat':food.fat
                })
        else:
            try:
                api_results = search_foods(search_term)
            except Exception:
                error_message = f"Couldn't connect to the food database: {search_term}, try again later."

    context = {
        'search_term': search_term,
        'api_results': api_results,
        'error_message': error_message,
    }
    return render(request, 'nutrieps/search.html', context)


@login_required
def profile(request):
    """Profile page view - P5 logic. Handles BMR calculation and profile updates."""

    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'weight': 0.0,
            'height': 0.0,
            'calories_goal': 0
        }
    )

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            activity_level = float(form.cleaned_data['activity_level'])
            goal_type = form.cleaned_data.get('goal_type', 'M')
            

            # 2. Perform calculations(Mifflin-St Jeor formula)
            if gender == 'M':
                tmb = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                tmb = (10 * weight) + (6.25 * height) - (5 * age) - 161

            base_calories = round(tmb * activity_level)

            # 3. Calculate the calories
            if goal_type == 'L':
                calculated_calories = base_calories - 300
            elif goal_type == 'G':
                calculated_calories = base_calories + 300
            else:
                calculated_calories = base_calories

            # 4. Save to database
            user_profile.goal_type = goal_type
            user_profile.weight = weight
            user_profile.height = height
            user_profile.age = age
            user_profile.activity_level = activity_level
            user_profile.calories_goal = calculated_calories
            user_profile.save()

            WeightLog.objects.create(
                user=request.user,
                weight=weight,
                date=timezone.now().date()
            )

    else:
        # 1. If user just visiting the page (GET request)
        form = UserProfileForm(
            # Initial information for help user
            initial={
                'age': user_profile.age,
                'weight': user_profile.weight,
                'height': user_profile.height,
                'gender': user_profile.gender,
                'activity_level': user_profile.activity_level,
                'goal_type': user_profile.goal_type,
            }
        )

    member_since = request.user.date_joined.strftime('%B %Y') 

    last_weight_log = WeightLog.objects.filter(user=request.user).order_by('-date').first()
    
    if last_weight_log:
        last_update = last_weight_log.date.strftime('%d/%m/%Y')
    else:
        last_update = "Never"

    context = {
        'profile_form': form,
        'current_profile': {
            'weight': user_profile.weight,
            'height': user_profile.height,
            'calories_goal': user_profile.calories_goal,
            'member_since': member_since,
            'last_update': last_update
        }
    }

    return render(request, 'nutrieps/profile.html', context)


@login_required
def history(request):
    """History page view - P6 logic. Real data from database"""

    # 1. Recuperar tot l'historial de menjars de l'usuari des del més recent al més antic
    logs = ConsumptionLog.objects.filter(user=request.user).select_related('food').order_by('-date')

    # Creem la llista tal com demana el Frontend (basant-nos en el mock i agrupant per dia naturalment)
    historical_records = []
    for log in logs:
        cals = (log.food.calories * log.quantity) / 100.0
        historical_records.append({
            'id': log.id,
            'date': log.date.strftime('%Y-%m-%d'),  # Ex: 2026-04-10
            'food': {'name': log.food.name},
            'quantity': log.quantity,
            'calories': round(cals, 1)
        })

    # 2. Historial de Pes
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('-date')
    weight_history = []
    for w_log in weight_logs:
        weight_history.append({
            'date': w_log.date.strftime('%Y-%m-%d'),
            'weight': w_log.weight
        })

    # 3. Calories d'avui
    today = timezone.now().date()
    todays_logs = ConsumptionLog.objects.filter(user=request.user, date=today).select_related('food')
    total_calories_today = sum((log.food.calories * log.quantity) / 100.0 for log in todays_logs)
    
    user_goal = 2000
    if hasattr(request.user, 'userprofile') and request.user.userprofile.calories_goal:
        user_goal = request.user.userprofile.calories_goal
        
    calories_pct = min(100, int((total_calories_today / user_goal) * 100)) if user_goal > 0 else 0

    # 4. Passar el diccionari al FrontEnd
    context = {
        'historical_records': historical_records,
        'weight_history': weight_history,
        'calories_today': round(total_calories_today),
        'calories_goal': round(user_goal),
        'calories_pct': calories_pct
    }
    return render(request, 'nutrieps/history.html', context)


@login_required
def add_consumption(request):
    """View to handle adding a food item to the consumption log via POST"""
    if request.method == 'POST':
        form = ConsumptionForm(request.POST)
        if form.is_valid():
            food, _ = FoodItem.objects.get_or_create(
                name=form.cleaned_data['food_name'],
                defaults={
                    'calories': form.cleaned_data['calories'],
                    'protein': form.cleaned_data.get('protein', 0.0) or 0.0,
                    'carbs': form.cleaned_data.get('carbs', 0.0) or 0.0,
                    'fat': form.cleaned_data.get('fat', 0.0) or 0.0
                }
            )

            ConsumptionLog.objects.create(
                user=request.user,
                food=food,
                quantity=form.cleaned_data['quantity']
            )

            return redirect('nutrieps:history')

    return redirect('nutrieps:search')


@login_required
def delete_consumption(request, log_id):
    """View to delete a consumption log"""
    if request.method == 'POST':
        log = ConsumptionLog.objects.filter(id=log_id, user=request.user).first()
        if log:
            log.delete()
    return redirect('nutrieps:history')


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
