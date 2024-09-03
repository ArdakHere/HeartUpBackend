from rest_framework import permissions, viewsets

from . import models, serializers


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = models.NotificationModel.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
