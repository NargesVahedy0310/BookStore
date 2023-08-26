from . import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import OTPRequest
from .serializers import VerifyOtpRequestSerializer
from rest_framework.permissions import AllowAny
class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = serializers.RequestOTPSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = OTPRequest.objects.generate(data)
                return Response(data=serializers.RequestOTPResponseSerializer(otp).data)
            except Exception as e:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def post(self, request):
        # Deserialize the request data using the VerifyOtpRequestSerializer
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # Check if the provided OTP is valid
            if OTPRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                # Handle user login and token generation
                user, token = self._handle_login(data)
                return Response({
                    'message': 'کاربر با موفقیت تایید شد.',
                    'user_id': user.id,
                    'token': token,
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'کد OTP نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def _handle_login(self, otp):
        User = get_user_model()
        query = User.objects.filter(username=otp['receiver'])
        if query.exists():
            user = query.first()
            # If the user exists, create a new JWT token
            refresh = RefreshToken.for_user(user)
            return user, str(refresh.access_token)
        else:
            user = User.objects.create(username=otp['receiver'])
            # If a new user is created, create a new JWT token
            refresh = RefreshToken.for_user(user)
            return user, str(refresh.access_token)
