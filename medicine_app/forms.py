from django import forms
from .models import Medicine, MedicineEvent, MedicineReminder, Person
from django.utils.translation import gettext_lazy as _

class MedicineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MedicineForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = ''

    class Meta:
        model = Medicine
        fields = ['name', 'doses', 'current_dose']
        labels = {
            'name': _('Namn'),
            'doses': _('Antal doser'),
            'current_dose': _('Nuvarande dos'),
        }

class MedicineReminderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        person = kwargs.pop('person', None)
        super().__init__(*args, **kwargs)
        if person is not None:
            self.fields['medicine'].queryset = Medicine.objects.filter(person=person)

    class Meta:
        model = MedicineReminder
        fields = ['medicine', 'time', 'active']
        labels = {
            'medicine': _('Medicin'),
            'time': _('Tid'),
            'active': _('Aktiv'),
        }
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

class MedicineEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        person = kwargs.pop('person', None)
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = ''
            if isinstance(visible.field, forms.ChoiceField):
                visible.field.empty_label = ""
        if person is not None:
            self.fields['medicine'].queryset = Medicine.objects.filter(person=person)

    class Meta:
        model = MedicineEvent
        fields = ['medicine', 'date', 'doses']
        labels = {
            'medicine': _('Medicin'),
            'date': _('Datum'),
            'doses': _('Doser'),
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
    
    def clean_person(self):
        data = self.cleaned_data['person']
        return data

    def clean_medicine(self):
        data = self.cleaned_data['medicine']
        return data
    
    def clean_date(self):
        data = self.cleaned_data['date']
        return data
    
    def clean_doses(self):
        data = self.cleaned_data['doses']
        return data

class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PersonForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    class Meta:
        model = Person
        fields = ['name']
        labels = {
            'name': _('Namn'),
        }