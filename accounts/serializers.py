from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

CUSTOMER = get_user_model()
class CustomerSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, min_length=8)
  class Meta:
    model = CUSTOMER
    fields = ( 'email', 'first_name', 'last_name', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  # @transaction.atomic
  def create(self, validated_data):
    with transaction.atomic():
      try:
        customer = CUSTOMER.objects.create_user(  
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        password=validated_data['password'],
        )
        return customer
      except Exception as e:
        print(e)
        raise serializers.ValidationError({
        'status': 'error',
        'message': 'Account not created successful',
        })

    
  