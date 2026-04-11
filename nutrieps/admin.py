from django.contrib import admin
from .models import UserProfile, WeightLog, FoodItem, ConsumptionLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'height', 'weight', 'calories_goal')
    search_fields = ('user__username',) # Search just for username (use of __ as is a foreign key)

@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'date')
    list_filter = ('date',)  # Filter for date
    search_fields = ('user__username',) # Search just for username (use of __ as is a foreign key)

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'carbs', 'fat')
    search_fields = ('name',)  # Search for food name

@admin.register(ConsumptionLog)
class ConsumptionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'quantity', 'date')
    list_filter = ('date', 'user')  # Filter for user and date
    search_fields = ('user__username', 'food__name')  # Search for user or food (use of __ as is a foreign key)