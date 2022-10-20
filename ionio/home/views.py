from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistration, UserLoginSerializer
from django.contrib.auth import authenticate

class UserRegistrationView(APIView):
    def post(self, request, format=None):
            data = request.data
            serializer = UserRegistration(data = data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    'msg': 'Success'
                })
            return Response({
                'msg': serializer.errors
            })

# class UserLoginView(APIView):
#      def post(self, request):
#          data = request.data
#          serializer = UserLoginSerializer(data = data)
#          if serializer.is_valid():
#              email = serializer.data.get('email')
#              password = serializer.data.get('password')
#              print(email)
#              user = authenticate(email = email, password =  password)
#              if user is not None:
#                  return Response({
#                      'msg': 'Logged In'
#                  })
#              return Response({
#                  'msg': 'User Doesnt Not Exist'
#              })
#          return Response({
#              'msg': serializer.errors,
#          })
class UserLoginView(APIView):
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      return Response({'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
