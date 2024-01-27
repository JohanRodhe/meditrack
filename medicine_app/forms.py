from django import forms
from .models import Medicine, Event

class MedicineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = Medicine
        fields = "__all__"


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['medicine'].queryset = Medicine.objects.filter(current_dose__gt=0)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
