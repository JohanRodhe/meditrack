from django.shortcuts import render
from .forms import MedicineForm, EventForm
from .models import Medicine
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods 
from django.contrib.auth.decorators import login_required
import datetime
from dateutil.relativedelta import relativedelta

DATE = datetime.datetime.now()

# Create your views here.
class MedicineList(ListView):
    model = Medicine
    template_name = "medicines.html"
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
    return render(request, "home.html", {"date": DATE})

def show_calendar(request):
    return render(request, "partials/calendar.html", {"date": DATE})
    
def create_medicine(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "partials/medicine_list.html", {"medicines": Medicine.objects.all()})
    else:
        form = MedicineForm()
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
    form = MedicineForm()
    return render(request, "partials/create_medicine_form.html", {"form": MedicineForm()})

def show_create_event_form(request):
    form = EventForm()
    return render(request, "partials/create_event_form.html", {"form": EventForm()})

def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "partials/calendar.html", {"date": DATE})
    else:
        form = EventForm()
    return render(request, "partials/calendar.html", {"date": DATE})

def view_next_month(request):
    global DATE
    DATE = DATE + relativedelta(months=+1)
    print(DATE)
    return render(request, "partials/calendar.html", {"date": DATE})

def view_prev_month(request):
    global DATE
    DATE = DATE + relativedelta(months=-1)
    print(DATE)
    return render(request, "partials/calendar.html", {"date": DATE})

def empty_view(request):
    return render(request, "partials/empty.html", {})