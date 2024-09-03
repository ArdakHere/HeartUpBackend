from django.urls import path

from . import views


urlpatterns = [
    path('', views.NotificationViewSet.as_view({'get': 'list'}), name='notifications'),
]
