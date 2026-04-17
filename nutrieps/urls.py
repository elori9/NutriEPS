# nutrieps/urls.py

from django.urls import path

from . import views

app_name = 'nutrieps'  # namespace: lets us write {% url 'blog:home' %} in templates

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    # Search for aliments
    path('search/', views.search, name='search'),
    # User profile
    path('profile/', views.profile, name='profile'),
    # User history
    path('history/', views.history, name='history'),
    # Add food to consumption log
    path('add-consumption/', views.add_consumption, name='add_consumption'),
    # Delete food from consumption log
    path('delete-consumption/<int:log_id>/', views.delete_consumption, name='delete_consumption'),
]