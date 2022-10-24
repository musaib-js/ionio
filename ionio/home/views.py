from django.shortcuts import HttpResponse
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistration, UserLoginSerializer, FileSerializer, FileSendSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Files, User
import json
from rest_framework.decorators import api_view

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)

  return{
    'refresh': str(refresh),
    'access': str(refresh.access_token)
  }

class UserRegistrationView(APIView):
    def post(self, request, format=None):
            data = request.data
            serializer = UserRegistration(data = data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token = get_tokens_for_user(user)
                print(token)

                return Response({
                    'msg': 'Success',
                    'token': token,
                })
            return Response({
                'msg': serializer.errors
            })

class UserLoginView(APIView):
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    print(user.email)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'bool': True, 'user': json.dumps(user.id), 'msg':'Login Success', 'token': token},  status=status.HTTP_200_OK)
    else:
      return Response({'bool': False, 'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class FileUploadView(APIView):
   permission_classes  =[IsAuthenticated]
   def post(self, request):
     data = request.data
     data['uploaded_by'] = int(data['uploaded_by'])
     print(data)
     serializer = FileSerializer(data = data)
     if serializer.is_valid():
       serializer.save()
       return Response({
         'msg': 'Successfully Uploaded',
         'data': serializer.data
       })
     return Response({
       'msg': serializer.errors
     })

class PreviousBatchFetch(APIView):
  def get(self, request, id):
    user = User.objects.filter(id = id)[0]
    uploads = Files.objects.filter(uploaded_by = user)
    serializer = FileSendSerializer(uploads, many = True)
    # print(serializer.data)
    return Response(serializer.data
    )

class ParseFile(APIView):
  def post(self, request):
    print(request.data)
    filetobeparsed = Files.objects.filter(file = request.data)
    print(filetobeparsed)
    return Response({
      'msg': 'received'
    })

@api_view(['GET'])
def show(request):
  # print(request.GET)
  with open(request.GET['name'], 'r') as f:
    return HttpResponse(f)
