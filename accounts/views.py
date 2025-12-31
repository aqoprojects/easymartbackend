from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import CustomerSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from cart.models import Cart, CartItems
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .authentication import CookieJWTAuthentication
from .serializers import LoginSerializer, CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from django.contrib.auth import logout as auth_logout
from .authentication import CookieJWTAuthentication
from utils.cart import find_guest_cart


CUSTOMER = get_user_model()
class customerRegisterationView(generics.CreateAPIView):
  serializer_class = CustomerSerializer

  def create(self, request, *args, **kwargs):
  
    print(request.data)
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    customer = serializer.save()
    print("VIEW USER SAVED")
    print(customer)
    return Response({
      "user": {
        "email": customer.email,
        "first_name": customer.first_name,
        "last_name": customer.last_name
      },
      "message": "Acccount created successfully uicv jjht ldfx qhln"
      }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token


                find_guest_cart(self, user)
                response = Response(
                    {'message': 'Login successful', 'user_id': user.customer_id},
                    status=status.HTTP_200_OK
                )

                response.delete_cookie(
                    'guest_id',  samesite='Lax', path='/'
                )
                response.set_cookie(
                    'access_token', str(access_token), httponly=True, secure=True, samesite='Lax', max_age=3600  # Adjusted for dev
                )
                response.set_cookie(
                    'refresh_token', str(refresh), httponly=True, secure=True, samesite='Lax', max_age=86400
                )

                return response
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):
    authentication_classes = [CookieJWTAuthentication]  # Explicit: Use cookie auth
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    authentication_classes = [CookieJWTAuthentication]  # Explicit: Use cookie auth
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            except TokenError:
                response = Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response({'error': 'No refresh token found'}, status=status.HTTP_400_BAD_REQUEST)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access (relies on refresh cookie)

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {'error': 'No refresh token in cookies'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)

            response = Response({'message': 'Token refreshed successfully'}, status=status.HTTP_200_OK)
            response.set_cookie(
                'access_token', new_access_token, httponly=True, secure=True, samesite='Lax', max_age=3600
            )

            # Rotate refresh token if configured (blacklists old one automatically via BLACKLIST_AFTER_ROTATION)
            response.set_cookie(
                'refresh_token', str(token), httponly=True, secure=True, samesite='Lax', max_age=86400
            )
            return response
        except TokenError:
            return Response(
                {'error': 'Invalid or expired refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
