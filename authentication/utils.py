# user/emails.py
import random
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

OTP_VALIDITY = timedelta(minutes=10)

class Util:
     @staticmethod
     def send_email(data):

            email = EmailMessage(
                subject=data["subject"],
                body=data["body"],
                from_email=settings.EMAIL_HOST_USER,
                to=[data["to_email"]],
            )

            email.send(fail_silently=False)
    
def send_verification_email(user, request=None):
    """
    Send email verification link using Django's built-in token generator
    Returns: (success: bool, message: str)
    """
    try:
        # Generate uid and token
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        
        # The email link itself must be a plain http(s) URL: most email
        # clients (Gmail included) only auto-linkify http(s), not custom
        # schemes like "myschool://", so a raw deep link is unclickable
        # text in the inbox. It points at VerifyEmailRedirectView, which in
        # turn hands off to the Flutter app's myschool://verify-email deep
        # link. Must use "uidb64" (not "uid") to match
        # VerifyEmailSerializer's expected field name.
        if request is not None:
            # 10.0.2.2 is the Android emulator's NAT alias for the host
            # machine's localhost: it's how the Flutter app running in the
            # emulator reaches the backend, but it's not a real address —
            # nothing outside the emulator (e.g. a browser on the dev
            # machine, where the verification email actually gets opened)
            # can resolve it. Swap it for localhost so the link is
            # clickable from wherever the email is read on the dev machine.
            host = request.get_host()
            if host.split(':')[0] == '10.0.2.2':
                host = 'localhost' + (f":{host.split(':', 1)[1]}" if ':' in host else '')
            scheme = 'https' if request.is_secure() else 'http'
            base_url = f"{scheme}://{host}{reverse('authentication:verify-email-redirect')}"
        else:
            base_url = getattr(
                settings,
                'EMAIL_VERIFICATION_URL',
                'http://localhost:8000/api/auth/verify-email-redirect/',
            )
        verification_url = f"{base_url}?uidb64={uid}&token={token}"

        # OTP alternative to the link: some clients (or desktop testing,
        # see the host-swap above) can't act on the link at all, so the app
        # lets the user type this code in directly instead.
        otp = f"{random.randint(0, 999999):06d}"
        user.verification_otp = otp
        user.verification_otp_expires_at = timezone.now() + OTP_VALIDITY
        user.save(update_fields=['verification_otp', 'verification_otp_expires_at'])

        # Email content
        subject = 'Verify Your Email Address'
        message = f"""
Hello {user.user_name or user.email},

Thank you for registering. Enter this code in the app to verify your email address:

{otp}

This code expires in 10 minutes.

Alternatively, click the link below to verify directly:

{verification_url}

This link will expire in 24 hours.

If you didn't create an account, please ignore this email.

Best regards,
Your App Team
"""
        
        # Send email using your existing Util class
        email_data = {
            'subject': subject,
            'body': message,
            'to_email': user.email,
        }
        Util.send_email(email_data)
        
        return True, "Verification email sent successfully"
        
    except Exception as e:
        return False, str(e)