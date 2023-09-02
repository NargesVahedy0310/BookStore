from enum import Enum
from circuitbreaker import CircuitBreaker

class SMSService(Enum):
    KAVENEGAR = "Kavenegar"
    SIGNAL = "Signal"

class SMSBreaker:
    def __init__(self):
        self.kavenegar_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
        self.signal_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
        self.current_service = SMSService.KAVENEGAR
        
    def send_sms_kavenegar(self, otp):
        try:
            print(f"Sending SMS via Kavenegar. OTP:=>  {otp.password}")
        except Exception as e:
            raise e

    def send_sms_signal(self, otp):
        try:
            print(f"Sending SMS via signal. OTP:=>  {otp.password}")
        except Exception as e:
            raise e

    def send_sms(self, otp):
        from.models import sms_breaker_status

        value_data = sms_breaker_status.objects.all().values()[0]['title_service']
        if value_data == "Kavenegar":
            try:
                self.kavenegar_breaker.call(self.send_sms_kavenegar, otp)
            except Exception as e:
                print(f"Kavenegar service failed. Switching to Signal.")

                status_instance = sms_breaker_status.objects.first()
                status_instance.title_service = sms_breaker_status.status_sms.SIGNAL
                status_instance.save()
                self.current_service = SMSService.SIGNAL
                self.signal_breaker.call(self.send_sms_signal, otp)
        else:
            try:
                self.signal_breaker.call(self.send_sms_signal, otp)
            except Exception as e:
                print(f"Signal service failed. Switching to Kavenegar.")
                status_instance = sms_breaker_status.objects.first()
                status_instance.title_service = sms_breaker_status.status_sms.KAVENEGAR
                status_instance.save()
                self.current_service = SMSService.KAVENEGAR
                self.kavenegar_breaker.call(self.send_sms_kavenegar, otp)
