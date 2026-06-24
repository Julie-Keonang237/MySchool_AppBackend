# user/emails.py
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class Util:
    @staticmethod
    def send_email(data):
        """Generic email sender"""
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']],
        )
        email.send()
    
def send_verification_email(user, request=None):
    """
    Send email verification link using Django's built-in token generator
    Returns: (success: bool, message: str)
    """
    try:
        # Generate uid and token
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        
        # Build verification URL for Flutter app
        # Change this to your Flutter app's deep link URL
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        verification_url = f"{frontend_url}/verify-email?uid={uid}&token={token}"
        
        # Email content
        subject = 'Verify Your Email Address'
        message = f"""
Hello {user.user_name or user.email},

Thank you for registering. Please click the link below to verify your email address:

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