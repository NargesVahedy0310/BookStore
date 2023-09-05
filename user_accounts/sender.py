import time 
from .circuitbreaker import SMSBreaker
sms_breaker = SMSBreaker(failure_threshold=3, recovery_timeout=30)

for _ in range(4):
    otp = 'OK'  
    sms_breaker.send_sms(otp)
    time.sleep(0.5)

sms_breaker.attempt_recovery()
