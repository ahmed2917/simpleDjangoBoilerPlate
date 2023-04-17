from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status

from .serializer import SignupSerializer, SigninSerializer
from utils.response import success_response, failed_response


class Signup(APIView):

    def post(self, *args, **kwargs):
        serialized_data = SignupSerializer(data=self.request.data)
        if serialized_data.is_valid():
            instance = serialized_data.save()
            response = success_response(None, "User signedup successfully", None, state=status.HTTP_200_OK)
            return Response(response)
        else:
            response = failed_response(None, serialized_data.errors, None, state=status.HTTP_400_BAD_REQUEST)
            return Response(response)
        
class Signin(APIView):

    def post(self, *args, **kwargs):
        serialized_data = SigninSerializer(data=self.request.data)
        if serialized_data.is_valid():
            user = authenticate(
                username = serialized_data.data.get('username', ''),
                password = serialized_data.data.get('password', ''),
                )
            if user:
                token, _  = Token.objects.get_or_create(user=user)
                data = {
                    "username" : serialized_data.data.get('username'),
                    "token" : str(token)
                } 
                response = success_response(data, "User signedin successfully", None, state=status.HTTP_200_OK)
                return Response(response)
            else:
                response = success_response(None, "Invalid login credentials", None, state=status.HTTP_401_UNAUTHORIZED)
                return Response(response)
        else:
            response = failed_response(None, serialized_data.errors, None, state=status.HTTP_400_BAD_REQUEST)
            return Response(response)
            