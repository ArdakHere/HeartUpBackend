from django.urls import path
from . import views

urlpatterns = [
    path('medication/', views.MedicationView.as_view(), name='medication_list'),
    path('medication/<int:pk>/', views.MedicationDetailView.as_view(), name='medication_detail'),
    path('prescription/', views.PrescriptionView.as_view(), name='prescription_list'),
    path('prescription/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription_detail'),
    path('diagnosis/', views.DiagnosisView.as_view(), name='diagnosis_list'),
    path('diagnosis/<int:pk>/', views.DiagnosisDetailView.as_view(), name='diagnosis_detail'),
    path('medical_image/', views.MedicalImageView.as_view(), name='medical_image_list'),
    path('medical_image/<int:pk>/', views.MedicalImageDetailView.as_view(), name='medical_image_detail'),
]
