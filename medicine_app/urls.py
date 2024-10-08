from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.home, name='home'),
    path('person/<int:pk>', views.home, name='home'),
    path('medicines-list', views.MedicineList.as_view(), name='medicine_list'),
    path('show-events/<str:date>', views.show_events, name='show_events'),
    path('create-medicine', views.create_medicine, name='create_medicine'),
    path('create-event', views.create_event, name='create_event'),
    path('delete-event/<int:pk>', views.delete_event, name='delete_event'),
    path('create-person', views.create_person, name='create_person'),
    path('delete-medicine/<int:pk>', views.delete_medicine, name='delete_medicine'),
    path('update-medicine/<int:pk>', views.update_medicine, name='update_medicine'),
    path('show-create-form', views.show_create_form, name='show_create_form'),
    path('show-create-event-form/<int:day>/', views.show_create_event_form, name='show_create_event_form'),
    path('view-next-month', views.view_next_month, name='view_next_month'),
    path('view-prev-month', views.view_prev_month, name='view_prev_month'),
    path('empty-view', views.empty_view, name='empty_view')
]