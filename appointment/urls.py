from django.urls import path

from . import views

urlpatterns = [
    path('', views.AppointmentModelListCreateView.as_view(), name='appointment'),
    path('<int:pk>/', views.AppointmentModelRetrieveUpdateDestroyView.as_view(), name='appointment-detail'),
    path('doctor-slots/', views.DoctorAvailabilityListCreateView.as_view(), name='doctor-slots'),
    path('doctor-slots/<int:pk>/', views.DoctorAvailabilityRetrieveUpdateDestroyView.as_view(),
         name='doctor-slots-detail'),
    path('create-time-slots/', views.CreateTimeSlotsView.as_view(), name='create-time-slots'),

    path('book-appointment/', views.BookAppointmentView.as_view(), name='book-appointment'),
    path('approve-appointment/', views.ApproveAppointmentView.as_view(), name='approve-appointment'),
    path('reject-appointment/', views.RejectAppointmentView.as_view(), name='reject-appointment'),
    path('approved/', views.ApprovedAppointmentsListView.as_view(), name='approved-appointments'),
    path('pending/', views.PendingAppointmentsListView.as_view(), name='pending-appointments'),
    path('rejected/', views.RejectedAppointmentsListView.as_view(), name='rejected-appointments'),
]
