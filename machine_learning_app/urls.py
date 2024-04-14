from django.urls import path
from . import views

urlpatterns = [
    path('heart-beat/', views.HeartBeatView.as_view(), name='heart-beat'),
    path('ecg/', views.ECGView.as_view(), name='ecg'),
    path('ucl/', views.UCLView.as_view(), name='ucl'),
    path('ml-diagnosis-history/', views.MLDiagnosisHistoryView.as_view(), name='ml-diagnosis-history'),
]