from . import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import OTPRequest, Accounnt
from .serializers import VerifyOtpRequestSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics


class OTPVerificationView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        serializer = serializers.RequestOTPSerializer(data=request.query_params)

        if serializer.is_valid():
            data = serializer.validated_data
            number_phone = str(data['receiver'])
            if data['pass_one'] == data['pass_two']:
                if len(number_phone) == 11 and number_phone.startswith('09'):
                    try:
                        otp = OTPRequest.objects.generate(data)
                        return Response(data=serializers.RequestOTPResponseSerializer(otp).data)
                    except Exception as e:
                        return Response({'error': 'خطای داخلی سرور'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({'error': 'شماره تلفن نامعتبر است!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'پسورد اول با پسورد دوم برابر نیست'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = VerifyOtpRequestSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['receiver'], data['request_id'], data['password'],
                                           data['first_name'], data['last_name'], data['pass_one'],
                                           data['pass_two']):
                user, token = self._handle_login(data)
                return Response({
                    'message': 'کاربر با موفقیت تایید شد.',
                    'user_id': user.id,
                    'token': token,
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'کد OTP نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _handle_login(self, otp):
        User = get_user_model()
        query = User.objects.filter(username=otp['receiver'])

        if query.exists():
            user = query.first()
        else:
            user = User.objects.create(
                username=otp['receiver'],
                first_name=otp['first_name'],
                last_name=otp['last_name']
            )
            user.set_password(otp['pass_one'])
            user.save()

        # ایجاد یک توکن جدید برای کاربر
        token, created = Token.objects.get_or_create(user=user)

        return user, str(token)

# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]  
#     def get(self, request):
#         user_profile = {
#             "username": request.user.username,
#             "first_name": request.user.first_name,
#             "last_name": request.user.last_name,
#         }

#         return Response(user_profile, status=status.HTTP_200_OK)

# class UserProfileView(generics.RetrieveAPIView):
#     serializer_class = AccountSerializers
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user