import random
from app.models import *
from rest_framework import status
from django.db import transaction
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from app.permissions import UserRolePermission
from app.task import send_emails,reg_send_emails
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from app.custom_email_backend import CustomEmailBackend
from rest_framework_simplejwt.tokens import RefreshToken
from app.serializers import UserSerializer,UserLimitedUpdateSerializer

# Create your views here.
# User Registration_Api
class UserRegistrationView(APIView):
    def post(self,request):
        try:
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                reg_send_emails.delay(serializer.data['username'], serializer.data['email'])
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    "Usedata": serializer.data,
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Update_Api
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, UserRolePermission]
    def put(self, request, id):
        try:
            user = Usercustome.objects.get(id=id)
            serializer = UserLimitedUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                with transaction.atomic():
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Usercustome.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Login_Api
class UserLoginView(APIView): 
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                otp = random.randint(1000, 9999)               
                cache.set(user.username, otp, timeout=300) 
                #Send OTP To User Email    
                send_emails.delay(otp, user.username, user.email)
                return Response({'refresh': str(refresh),'access': str(refresh.access_token),
                    "Usedata": {'username': user.username,}
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Otp Verify_Api
class VerifyOtpView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            username = request.data.get('username')
            input_otp = str(request.data.get('otp'))
            if  username and input_otp:
                cache_key = username  #Use username as cachekey   
                cached_otp = cache.get(cache_key)
            else:
                return Response({"error": "Username and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)
            if cached_otp is None:
                return Response({"error": "OTP expired or invalid. Please request a new one"}, status=status.HTTP_400_BAD_REQUEST)
            if str(cached_otp) != input_otp:
                return Response({"error": "Invalid OTP. Please try again"}, status=status.HTTP_400_BAD_REQUEST)
            cache.delete(cache_key)  # delete OTP immediately
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        except Exception as e:            
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Password Reset_Api
class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            if not username or not password:
                return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
            if len(password) < 6:
                return Response({"error": "Password must be at least 6 characters long."}, status=status.HTTP_400_BAD_REQUEST)
            user = Usercustome.objects.get(username=username)
            with transaction.atomic():
                user.set_password(password)
                user.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        except Usercustome.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
