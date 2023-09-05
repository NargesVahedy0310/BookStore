import random
import time
from .sms_service import SMSService

class SMSBreaker:
    def __init__(self, failure_threshold, recovery_timeout):
        self.services = [SMSService.KAVENEGAR, SMSService.SIGNAL, SMSService.MELISMS]
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.current_service = SMSService.KAVENEGAR
        self.kavenegar_failure_count = 0
        self.signal_failure_count = 0
        self.melisms_failure_count = 0
        self.kavenegar_last_failure_time = 0
        self.signal_last_failure_time = 0
        self.melisms_last_failure_time = 0
        self.default_service_blocked_time = 0
        
    def send_sms_kavenegar(self, otp):
        try:
            if not self.is_service_blocked(SMSService.KAVENEGAR):
                print(f"Sending SMS via Kavenegar. OTP: {otp.password}")
            else:
                print("Kavenegar service is blocked. Switching to another service.")
                self.switch_to_random_service()
        except Exception as e:
            print(f"Error sending SMS via Kavenegar: {str(e)}")
            self.handle_failure(SMSService.KAVENEGAR)

    def send_sms_signal(self, otp):
        try:
            if not self.is_service_blocked(SMSService.SIGNAL):
                print(f"Sending SMS via Signal. OTP: {otp}")
            else:
                print("Signal service is blocked. Switching to another service.")
                self.switch_to_random_service()
        except Exception as e:
            print(f"Error sending SMS via Signal: {str(e)}")
            self.handle_failure(SMSService.SIGNAL)

    def send_sms_melisms(self, otp):
        try:
            if not self.is_service_blocked(SMSService.MELISMS):
                print(f"Sending SMS via Melisms. OTP: {otp}")
            else:
                print("Melisms service is blocked. Switching to another service.")
                self.switch_to_random_service()
        except Exception as e:
            print(f"Error sending SMS via Melisms: {str(e)}")
            self.handle_failure(SMSService.MELISMS)

    def send_sms(self, otp):
        # Kavenegar
        current_time = time.time()
        if self.current_service == SMSService.KAVENEGAR:
            if current_time - self.default_service_blocked_time >= self.recovery_timeout:
                self.current_service = SMSService.KAVENEGAR
                print("Default service Kavenegar has been recovered.")
        available_services = [s for s in self.services if not self.is_service_blocked(s)]
        if available_services:
            selected_service = random.choice(available_services)
            if selected_service == SMSService.KAVENEGAR:
                self.send_sms_kavenegar(otp)
            elif selected_service == SMSService.SIGNAL:
                self.send_sms_signal(otp)
            elif selected_service == SMSService.MELISMS:
                self.send_sms_melisms(otp)
        else:
            print("All services are blocked. Please wait for recovery.")

    def is_service_blocked(self, service):
        if service == SMSService.KAVENEGAR:
            return self.kavenegar_failure_count >= self.failure_threshold
        elif service == SMSService.SIGNAL:
            return self.signal_failure_count >= self.failure_threshold
        elif service == SMSService.MELISMS:
            return self.melisms_failure_count >= self.failure_threshold
        return False

    def handle_failure(self, service):
        if service == SMSService.KAVENEGAR:
            self.kavenegar_failure_count += 1
            self.kavenegar_last_failure_time = time.time()
            if self.kavenegar_failure_count >= self.failure_threshold:
                print("Kavenegar service is blocked. Switching to Signal.")
                self.switch_to_random_service()
        elif service == SMSService.SIGNAL:
            self.signal_failure_count += 1
            self.signal_last_failure_time = time.time()
            if self.signal_failure_count >= self.failure_threshold:
                print("Signal service is blocked. Switching to Kavenegar.")
                self.switch_to_random_service()
        elif service == SMSService.MELISMS:
            self.melisms_failure_count += 1
            self.melisms_last_failure_time = time.time()
            if self.melisms_failure_count >= self.failure_threshold:
                print("Melisms service is blocked. Switching to another service.")
                self.switch_to_random_service()
        
    def reset_failure_count(self, service):
        if service == SMSService.KAVENEGAR:
            self.kavenegar_failure_count = 0
        elif service == SMSService.SIGNAL:
            self.signal_failure_count = 0
        elif service == SMSService.MELISMS:
            self.melisms_failure_count = 0

    def switch_to_random_service(self):
        available_services = [s for s in self.services if not self.is_service_blocked(s)]
        if available_services:
            new_service = random.choice(available_services)
            self.current_service = new_service
            print(f"Switched to {new_service} service.")
        else:
            print("All services are blocked. Please wait for recovery.")

    def attempt_recovery(self):
        print("Attempting to recover services...")
        for service in self.services:
            if service == SMSService.KAVENEGAR:
                recovery_time = time.time() - self.kavenegar_last_failure_time
                if recovery_time >= self.recovery_timeout:
                    self.reset_failure_count(service)
                    print(f"{service.value} service has been recovered.")
            else:
                recovery_time = 0
                if service == SMSService.SIGNAL:
                    recovery_time = time.time() - self.signal_last_failure_time
                elif service == SMSService.MELISMS:
                    recovery_time = time.time() - self.melisms_last_failure_time

                if recovery_time >= self.recovery_timeout:
                    self.reset_failure_count(service)
                    print(f"{service.value} service has been recovered.")
