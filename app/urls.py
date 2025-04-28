from django.urls import path
from app.views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('userreg', UserRegistrationView.as_view(), name='userreg'),
    path('userlogin', UserLoginView.as_view(), name='userlogin'),
    path('otpverify', VerifyOtpView.as_view(), name='otpverify'),
    path('passwordreset', PasswordResetView.as_view(), name='passwordreset'),   
    path('userupdate/<int:id>', UserUpdateView.as_view(), name='userupdate'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


