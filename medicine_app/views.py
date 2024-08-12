from django.shortcuts import redirect, render
from .forms import MedicineForm, MedicineEventForm, PersonForm
from .models import Medicine, MedicineEvent, Person
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods 
from django.contrib.auth.decorators import login_required
import datetime
from dateutil.relativedelta import relativedelta

DATE = datetime.datetime.now()

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
        person_id = self.request.session.get("current_person_id")
        person = Person.objects.filter(pk=person_id).first()

        return Medicine.objects.filter(person=person)

def index(request):
    return render(request, "index.html", {})

@login_required
def home(request, pk=None):
    user = request.user
    persons = Person.objects.filter(user=user)

    person_id = pk or request.session.get("current_person_id")

    if person_id is None and persons.exists():
        person_id = persons.first().pk
    
    person = persons.filter(pk=person_id).first()

    request.session["current_person_id"] = person_id

    medicines = Medicine.objects.filter(person=person)
    events = MedicineEvent.objects.filter(person=person, date__month=DATE.month)

    return render(request, "home.html",
                    {
                        "date": DATE,
                        "person": person,
                        "persons": persons,
                        "medicines": medicines,
                        "events": events
                    })


@login_required
def create_medicine(request):
    person_id = request.session.get("current_person_id")
    person = Person.objects.filter(pk=person_id).first()
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.person = person
            medicine.save()
    else:
        form = MedicineForm(user=request.user)

    return redirect('medicine_list')

@login_required
def update_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    if request.method == "POST":
        medicine.current_dose = medicine.current_dose + 1
        medicine.save()

    return redirect('medicine_list')


@require_http_methods(["DELETE"])
def delete_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    medicine.delete()

    return redirect('medicine_list')

def show_create_form(request):
    return render(request, "partials/create_medicine_form.html", {"form": MedicineForm(user=request.user)})

@login_required
def show_create_event_form(request, day):
    person_id = request.session.get("current_person_id")
    person = Person.objects.filter(pk=person_id).first()
    form = MedicineEventForm(person=person)
    if day:
        new = DATE.replace(day=day)
        form.fields["date"].initial = new
    else:
        form.fields["date"].initial = DATE
    
    events = MedicineEvent.objects.filter(person=person, date=new)
    return render(request, "partials/create_event_form.html", {"form": form, "events": events, "date": new})

@login_required
def create_event(request):
    person_id = request.session.get("current_person_id")
    person = Person.objects.filter(pk=person_id).first()
    if request.method == "POST":
        form = MedicineEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            MedicineEvent.create_event(person, event.medicine, event.date, event.doses)
            events = MedicineEvent.objects.filter(person=person, date=event.date)
            response = render(request, "partials/day_button.html", {"day": event.date.day, "events": events})
            response['HX-Trigger'] = 'new_med_event'
            return response
    else:
        form = MedicineEventForm()

    medicines = Medicine.objects.filter(person=person)
    return render(request, "home.html", {"date": DATE, "medicines": medicines }) 

@login_required
def view_next_month(request):
    global DATE
    DATE = DATE + relativedelta(months=+1)
    person_id = request.session.get("current_person_id")
    person = Person.objects.filter(pk=person_id).first()
    events = MedicineEvent.objects.filter(person=person, date__month=DATE.month)
    return render(request, "partials/calendar.html", {"date": DATE, "events": events})

@login_required
def view_prev_month(request):
    global DATE
    DATE = DATE + relativedelta(months=-1)
    person_id = request.session.get("current_person_id")
    person = Person.objects.filter(pk=person_id).first()
    events = MedicineEvent.objects.filter(person=person, date__month=DATE.month)
    return render(request, "partials/calendar.html", {"date": DATE, "events": events})

def empty_view(request):
    return render(request, "partials/empty.html", {})

@login_required
def create_person(request):
    if (request.POST):
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            request.session["current_person_id"] = person.pk
            return render(request, "partials/person.html", {"person": person})
    else:
        form = PersonForm(user=request.user)
    return render(request, "partials/create_person_form.html", {"form": form})