from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_app.api.serializers import RegistrationSerializer


@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        ser = RegistrationSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)

        return Response(ser.errors)