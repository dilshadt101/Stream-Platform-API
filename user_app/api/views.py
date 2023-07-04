from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from user_app.api.serializers import RegistrationSerializer
from user_app import models


@api_view(['POST'])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        ser = RegistrationSerializer(data=request.data)

        data = {}

        if ser.is_valid():
            account = ser.save()
            data['response'] = "Registration successful"
            data['username'] = account.username
            data['email'] = account.email

            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = ser.errors

        return Response(data)

