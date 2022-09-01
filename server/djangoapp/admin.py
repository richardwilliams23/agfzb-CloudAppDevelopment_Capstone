from django.contrib import admin
from .models import CarMake, CarModel

# Register models here

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [CarModelInline]

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['make', 'name', 'id', 'type', 'year']
    list_filter = ['type', 'make', 'id', 'year',]
    search_fields = ['make', 'name']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
