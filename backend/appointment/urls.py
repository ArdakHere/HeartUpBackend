from django.urls import path

from . import views

urlpatterns = [
    path('', views.AppointmentModelListCreateView.as_view(), name='appointment'),
    path('<int:pk>/', views.AppointmentModelRetrieveUpdateDestroyView.as_view(), name='appointment-detail'),
    path('doctor-slots/', views.DoctorAvailabilityListCreateView.as_view(), name='doctor-slots'),
    path('doctor-slots/<int:pk>/', views.DoctorAvailabilityRetrieveUpdateDestroyView.as_view(),
         name='doctor-slots-detail'),
    path('doctor-slots-by-id/<int:doctor_id>', views.SlotsByDoctorIdView.as_view(), name='doctor-slots-by-id'),
    path('doctor-slots-by-id-date/<int:doctor_id>/<str:date>/', views.SlotsByDoctorIdAndDateView.as_view(), name='doctor-slots-by-id-date'),
    path('create-time-slots/', views.DoctorTimeSlotsView.as_view(), name='create-time-slots'),

    path('book-appointment/', views.BookAppointmentView.as_view(), name='book-appointment'),
    path('approve-appointment/', views.ApproveAppointmentView.as_view(), name='approve-appointment'),
    path('reject-appointment/', views.RejectAppointmentView.as_view(), name='reject-appointment'),
    path('approved/', views.ApprovedAppointmentsListView.as_view(), name='approved-appointments'),
    path('pending/', views.PendingAppointmentsListView.as_view(), name='pending-appointments'),
    path('rejected/', views.RejectedAppointmentsListView.as_view(), name='rejected-appointments'),

    # For patient
    path('approved/my/', views.MyApprovedAppointmentsListView.as_view(), name='my-approved-appointments'),
    path('pending/my/', views.MyPendingAppointmentsListView.as_view(), name='my-pending-appointments'),
    path('rejected/my/', views.MyRejectedAppointmentsListView.as_view(), name='my-rejected-appointments'),

    # For doctor
    path('approved/my-doctor/', views.MyApprovedAppointmentsListDoctorView.as_view(), name='doctor-approved-appointments'),
    path('pending/my-doctor/', views.MyPendingAppointmentsListDoctorView.as_view(), name='doctor-pending-appointments'),
    path('rejected/my-doctor/', views.MyRejectedAppointmentsListDoctorView.as_view(), name='doctor-rejected-appointments'),

    path('busy-slots/<int:doctor_id>/', views.ApprovedAppointmentsByDoctorView.as_view(), name='busy-slots'),

    path('time-slots-by-date/', views.DoctorTimeSlotsByDateView.as_view(), name='time-slots-by-date'),
]
