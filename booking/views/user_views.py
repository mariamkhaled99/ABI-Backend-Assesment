# bookings/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse
from booking.models.user_models import CustomUser
from booking.serializers import  RegisterSerializer, LoginSerializer


@extend_schema(
    summary="Register a new user",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(description="User registered successfully"),
        400: OpenApiResponse(description="Bad request, email already in use")
    }
)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"status": f"User {user.first_name} registered successfully."}, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Login a user",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(description="User logged in successfully"),
        401: OpenApiResponse(description="Invalid credentials")
    }
)
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'first_name': user.first_name,
                'email': email,
                'id': user.pk
            }, status=status.HTTP_200_OK)
        return Response({"status": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
