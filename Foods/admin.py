from django.contrib import admin

# Register your models here.
from Foods.models import Food


class FoodAdmin(admin.ModelAdmin):
    list_display = ['food_name', 'food_purine', 'food_calories']


admin.site.register(Food, FoodAdmin)
