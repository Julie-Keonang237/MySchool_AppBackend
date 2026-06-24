# user/tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Generates secure tokens for email verification.
    This extends Django's built-in PasswordResetTokenGenerator.
    """
    def _make_hash_value(self, user, timestamp):
        """
        Create a hash value that includes:
        - User's primary key
        - Current timestamp (for expiration)
        - User's email (so token invalid if email changes)
        - User's is_active status (so token invalid after verification)
        """
        return (
            six.text_type(user.pk) + 
            six.text_type(timestamp) + 
            six.text_type(user.email) +
            six.text_type(user.is_active)
        )

# Create a single instance to use throughout your app
email_verification_token = EmailVerificationTokenGenerator()