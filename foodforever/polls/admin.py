from django.contrib import admin

from .models import Choice, Ingredient


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class IngredientAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['ingredient_name']}),
        ('Date information', {'fields': ['exp_date'], 'classes': ['collapse']}),
        ('Owner', {'fields': ['owner']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('ingredient_name', 'exp_date')
    list_filter = ['exp_date']
    search_fields = ['ingredient_name']

admin.site.register(Ingredient, IngredientAdmin)
