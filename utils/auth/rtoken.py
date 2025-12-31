# yourapp/utils.py   ← create this file
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)

    token[api_settings.USER_ID_CLAIM] = str(user.customer_id)

    # token['username'] = user.username
    token['email'] = user.email

    return token


def get_refresh_token_for_user(user):
  refresh = RefreshToken()
  refresh[api_settings.USER_ID_CLAIM] = str(user.customer_id)
  return refresh