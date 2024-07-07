from django.shortcuts import render
from .forms import MedicineForm, MedicineEventForm, PersonForm
from .models import Medicine, MedicineEvent, Person
from accounts.models import User 
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods 
from django.contrib.auth.decorators import login_required
import datetime
from dateutil.relativedelta import relativedelta

DATE = datetime.datetime.now()

# Create your views here.
class MedicineList(ListView):
    model = Medicine
    template_name = "partials/medicine_list.html"
    context_object_name = "medicines"

    def get_context_data(self, **kwargs):
        global DATE
        context = super(MedicineList, self).get_context_data(**kwargs)
        context["form"] = MedicineForm()
        context["date"] = DATE
        return context
    
    def get_queryset(self):
        return Medicine.objects.all()

def index(request):
    return render(request, "index.html", {})

@login_required
def home(request):
    user = request.user
    events = MedicineEvent.objects.filter(medicine__person__user=user)
    persons = Person.objects.filter(user=user)
    # TODO: Clicking on a person should show their medicines and events
    if (len(persons) == 0):
        medicines=[]
    else:
        medicines = Medicine.objects.filter(person=persons[0])

    return render(request, "home.html",
                    {
                        "date": DATE,
                        "persons": persons,
                        "medicines": medicines,
                        "events": events
                    })


def create_medicine(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "partials/medicine_list.html", {"medicines": Medicine.objects.all()})
    else:
        form = MedicineForm(user=request.user)
    return render(request, "partials/medicine_list.html", {"medicines": Medicine.objects.all()})

def update_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    if request.method == "POST":
        medicine.current_dose = medicine.current_dose + 1
        medicine.save()


    return render(request, "partials/medicine_list.html", {"medicines": Medicine.objects.all()})


@require_http_methods(["DELETE"])
def delete_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    medicine.delete()
    return render(request, 'partials/medicine_list.html', {'medicines': Medicine.objects.all()})

def show_create_form(request):
    return render(request, "partials/create_medicine_form.html", {"form": MedicineForm(user=request.user)})

@login_required
def show_create_event_form(request, day=None):
    form = MedicineEventForm()
    if day:
        new = DATE.replace(day=day)
        form.fields["date"].initial = new
    else:
        form.fields["date"].initial = DATE
    

    user = request.user
    events = MedicineEvent.objects.filter(date=new)
    return render(request, "partials/create_event_form.html", {"form": form, "events": events, "date": new})

@login_required
def create_event(request):
    if request.method == "POST":
        form = MedicineEventForm(request.POST)
        if form.is_valid():
            form.save()
            med = form.cleaned_data["medicine"]
            doses = form.cleaned_data["doses"]
            med.current_dose += doses
            med.save()
            event_date = form.cleaned_data["date"]
            events = MedicineEvent.objects.filter(date=event_date)
            response = render(request, "partials/day_button.html", {"day": event_date.day, "events": events})
            response['HX-Trigger'] = 'new_med_event'
            return response
    else:
        form = MedicineEventForm()

    user = request.user
    persons = Person.objects.filter(user=user)
    if (len(persons) == 0):
        medicines=[]
    else:
        medicines = Medicine.objects.filter(person=persons[0])
    return render(request, "home.html", {"date": DATE, "medicines": medicines }) 

def view_next_month(request):
    global DATE
    DATE = DATE + relativedelta(months=+1)
    return render(request, "partials/calendar.html", {"date": DATE})

def view_prev_month(request):
    global DATE
    DATE = DATE + relativedelta(months=-1)
    return render(request, "partials/calendar.html", {"date": DATE})

def empty_view(request):
    return render(request, "partials/empty.html", {})

def create_person(request):
    if (request.POST):
        form = PersonForm(request.POST)
        print("create person", form.is_valid())
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            return render(request, "partials/person.html", {"name" : form.cleaned_data["name"]})
    else:
        form = PersonForm(user=request.user)
    return render(request, "partials/create_person_form.html", {"form": form})