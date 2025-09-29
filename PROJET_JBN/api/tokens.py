from django.contrib.auth.tokens import PasswordResetTokenGenerator

class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Pa itilize last_login ni date_joined
        return str(user.pk) + str(timestamp) + str(user.actif)

custom_token_generator = CustomTokenGenerator()
