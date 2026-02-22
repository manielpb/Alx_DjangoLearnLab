from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Unread first, then newest
        return (
            Notification.objects
            .filter(recipient=self.request.user)
            .order_by("is_read", "-timestamp")
        )


class MarkAllNotificationsReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({"detail": "All notifications marked as read."}, status=status.HTTP_200_OK)
