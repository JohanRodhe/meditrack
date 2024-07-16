from django.contrib import admin

from accounts.models import User
from medicine_app.models import Medicine, MedicineEvent, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'doses', 'current_dose', 'person')

@admin.register(MedicineEvent)
class MedicineEventAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'date', 'doses', 'person')

# Register your models here.
admin.site.register(User)



