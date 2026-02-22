from django.urls import path, include
from .views import RegisterView, LoginView, UserViewSet,UnfollowUserView,FollowUserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
     path("follow/<int:user_id>", FollowUserView.as_view(), name="followuser"),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view(), name="unfollowuser"),
]
