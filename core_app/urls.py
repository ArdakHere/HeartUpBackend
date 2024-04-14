from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.PatientView.as_view(), name='core_app'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('doctors/', views.DoctorView.as_view(), name='doctor'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('appointment/', views.AppointmentView.as_view(), name='appointment'),
]
