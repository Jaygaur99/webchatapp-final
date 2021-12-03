import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    otp = random.randint(100000, 999999)
    return otp

def generate_otp_mail_fields(otp, fname):
    subject = "Password Change OTP"
    message = f"""Hey {fname}

We noticed that you are trying to change your password.
Your verification otp for changing password is {otp}.

Please do not disclose or share this one time password (otp) with others.
"""
    return subject, message

def send_mail_helper(subject, body, mail):
    send_mail(subject, body, settings.EMAIL_HOST_USER, [mail, ])

if __name__ == '__main__':
    print(generate_otp())
    sender, message = generate_otp_mail_fields(12456, "Jay")
    send_mail_helper(sender, message, 'jaygaur99@gmail.com')