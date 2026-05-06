from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from .services import logout_user, send_password_reset_mail, reset_user_password, blacklist_all_user_tokens

User = get_user_model()


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginApiView(TokenObtainPairView):
    """
    In this view,
    rest_framework_simplejwt will handle validation and authenticate user.
    then generate & return tokens.
    """
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")

        if not refresh:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            logout_user(refresh)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Logged out"})


class UpdateUserView(APIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.context["user"]
        send_password_reset_mail(user)

        return Response({"message": "Reset link sent"})


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        password = serializer.validated_data["password"]

        reset_user_password(user, password)

        # 🔥 Important: logout all devices
        # why? ---> because even after changing passowrd tokens are still valid. Which is not best practice.
        # so, you should blacklist all tokens of user.
        blacklist_all_user_tokens(user)

        return Response({"message": "Password reset successful"})
