from rest_framework import serializers
from .models import OTPRequest


class RequestOTPSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50, allow_null=False)
    channel = serializers.ChoiceField(allow_null=False, choices=OTPRequest.OtpChannel.choices)
    first_name = serializers.CharField(max_length=50, allow_null=False)
    last_name = serializers.CharField(max_length=50, allow_null=False)
    pass_one = serializers.CharField(max_length=15, allow_null=False)
    pass_two = serializers.CharField(max_length=15, allow_null=False)


class RequestOTPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ['request_id']

class VerifyOtpRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null=False)
    password = serializers.CharField(max_length=4, allow_null=False)
    receiver = serializers.CharField(max_length=64, allow_null=False)
    first_name = serializers.CharField(max_length=50, allow_null=False)
    last_name = serializers.CharField(max_length=50, allow_null=False)
    pass_one = serializers.CharField(max_length=15, allow_null=False)
    pass_two = serializers.CharField(max_length=15, allow_null=False)

class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
    created = serializers.BooleanField()