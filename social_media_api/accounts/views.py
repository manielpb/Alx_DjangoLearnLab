from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .models import User
from notifications.utils import create_notification

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token":token.key,
                "user": UserSerializer(user).data
            },
            status = status.HTTP_201_CREATED
        )
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user).data
            }
        )
    
User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only user listing/detail, plus follow/unfollow actions for authenticated users.
    """
    queryset = User.objects.all()
    # You can plug in your own User serializer here if you already have one.
    # serializer_class = UserSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        target = self.get_object()
        me = request.user

        if target == me:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        if me.following.filter(pk=target.pk).exists():
            return Response({"detail": "Already following."},
                            status=status.HTTP_200_OK)

        me.following.add(target)
        return Response({"detail": f"You are now following {target.username}."},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        target = self.get_object()
        me = request.user

        if target == me:
            return Response({"detail": "You cannot unfollow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not me.following.filter(pk=target.pk).exists():
            return Response({"detail": "You are not following this user."},
                            status=status.HTTP_200_OK)

        me.following.remove(target)
        return Response({"detail": f"You unfollowed {target.username}."},
                        status=status.HTTP_200_OK)
    

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def post(self, request, user_id):
        me = request.user
        target = get_object_or_404(User, id=user_id)

        if target == me:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if me.following.filter(id=target.id).exists():
            return Response(
                {"detail": "Already following this user."},
                status=status.HTTP_200_OK,
            )

        me.following.add(target)
        return Response(
            {"detail": f"You are now following {target.username}."},
            status=status.HTTP_201_CREATED,
        )


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def post(self, request, user_id):
        me = request.user
        target = get_object_or_404(User, id=user_id)

        if target == me:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not me.following.filter(id=target.id).exists():
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_200_OK,
            )

        me.following.remove(target)
        return Response(
            {"detail": f"You unfollowed {target.username}."},
            status=status.HTTP_200_OK,
        )
    

create_notification(
    recipient=target,
    actor=me,
    verb="started following you",
    target=None
)

create_notification(
    recipient=post.author,
    actor=user,
    verb="liked your post",
    target=post
)

def perform_create(self, serializer):
    comment = serializer.save(author=self.request.user)
    create_notification(
        recipient=comment.post.author,
        actor=self.request.user,
        verb="commented on your post",
        target=comment.post
    )