from django import forms
from .models import Medicine, MedicineEvent, Person
from django.utils.translation import gettext_lazy as _

class MedicineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MedicineForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['person'].queryset = user.person_set.all()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            # visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = Medicine
        fields = "__all__"
        labels = {
            'name': _('Namn'),
            'doses': _('Antal doser'),
            'current_dose': _('Nuvarande dos'),
        }


class MedicineEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if isinstance(visible.field, forms.ChoiceField):
                visible.field.empty_label = ""

    class Meta:
        model = MedicineEvent
        fields = "__all__"
        labels = {
            'medicine': _('Medicin'),
            'date': _('Datum'),
            'doses': _('Doser'),
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


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