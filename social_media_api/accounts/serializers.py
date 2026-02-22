from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "bio", "profile_picture"]

    def create(self, validated_data):
      user = get_user_model().objects.create_superuser(
          username=validated_data["username"],
          email=validated_data.get("email"),
          password=validated_data["password"],
          bio=validated_data.get("bio", ""),
          profile_picture=validated_data.get("profile_picture", None),
      )

      Token.objects.create(user=user)

      return user
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data
    
class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["id", "username", "email", "bio", "profile_picture"]