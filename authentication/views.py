from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from authentication.serializers import LoginSerializer, RegisterSerializer



# Create your views here.

class AuthUserAPIView(GenericAPIView):
     # need to set it to let django not to require jwt
    authentication_classes = []
    
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        user = request.user

        print(user,'user__')

        serializer = RegisterSerializer(user)
        return response.Response({'user': serializer.data})

        

class RegisterAPIView(GenericAPIView):
    serializer_class=RegisterSerializer

    def post(self,request):
        serializer =self.serializer_class(data=request.data)

        print(serializer,'__')

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    # need to set it to let django not to require jwt
    authentication_classes = []

    serializer_class=LoginSerializer

    def post(self, request):
        email= request.data.get('email', None)
        password= request.data.get('password',None)
 
        user=authenticate(username=email,password=password)
        print(user,'user')

        if user:
            serializer = self.serializer_class(user)

            return response.Response(serializer.data,status=status.HTTP_200_OK)
        return response.Response({'message':'Invalid credentials,try again'},status=status.HTTP_401_UNAUTHORIZED)



