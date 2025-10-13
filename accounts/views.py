from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import CustomerSerializer
from rest_framework import status

CUSTOMER = get_user_model()
class customerRegisterationView(generics.CreateAPIView):
  serializer_class = CustomerSerializer

  def create(self, request, *args, **kwargs):
  
    print(request.data)
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    customer = serializer.save()
    print("VIEW USER SAVED")
    print(customer)
    return Response({
      "user": {
        "email": customer.email,
        "first_name": customer.first_name,
        "last_name": customer.last_name
      },
      "message": "Acccount created successfully uicv jjht ldfx qhln"
      }, status=status.HTTP_201_CREATED)
    

