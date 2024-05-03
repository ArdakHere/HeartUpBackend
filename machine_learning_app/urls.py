from django.urls import path
from . import views

urlpatterns = [
    path('heart-beat/', views.HeartBeatView.as_view(), name='heart-beat'),
    path('ecg/', views.ECGView.as_view(), name='ecg'),
    path('ucl/', views.UCLView.as_view(), name='ucl'),
    path('echo-net/', views.EchoNetView.as_view(), name='echo-net'),
    path('ml-diagnosis-history/', views.MLDiagnosisView.as_view(), name='ml-diagnosis-history'),
    path('ml-diagnosis-history/<int:pk>/', views.MLDiagnosisDetailView.as_view(), name='ml-diagnosis-history-detail'),
    path('ml-diagnosis-history/patient/<int:patient>/', views.MLDiagnosisDetailByPatientView.as_view(), name='ml-diagnosis-history-patient'),
]
