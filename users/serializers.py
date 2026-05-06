from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# Login Serializer
class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for Login

    It requires 2 fields:
        1. get_user_model().USERNAME_FIELD : In our case is -> Email
        2, password
    """

    @classmethod
    def get_token(cls, user):
        """
        Que: Why this method Inherited from TokenObtainPairSerializer ??
        Ans: To customize the token payload.

        - By default, djangorestframework-simplejwt only includes minimal data in the payload.
        i.e
            {
              "user_id": 1,
              "exp": 1712345678,
              "jti": "random-id"
            }


        - After customization, Now your payload becomes:
            {
              "user_id": 1,
              "email": "user@example.com",
              "exp": 1712345678,
              "jti": "random-id"
            }
        """
        token = super().get_token(user)
        token["email"] = user.email
        return token


# Update User
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]  # only name fields can get updated for now.


# Forgot Password
class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email__iexact=value).first()
        if not user:
            raise serializers.ValidationError("User does not exist")
        self.context["user"] = user
        return value


# Reset password
class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(min_length=6)

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uid"]))
            user = User.objects.get(id=uid)
        except:
            raise serializers.ValidationError("Invalid user")

        if not PasswordResetTokenGenerator().check_token(user, attrs["token"]):
            raise serializers.ValidationError("Invalid or expired token")

        attrs["user"] = user
        return attrs
