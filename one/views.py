import email
from re import U
#import request
from django.conf import settings
from demo.settings import EMAIL_HOST_USER
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .models import *   
from rest_framework import viewsets
#from .serializers import UserSerializer
from django.core.mail import send_mail
from django.db.models import F, Value as V
from .serializers import RegisterSerializer,LoginSerializer, UserSerializer
from django.contrib.auth.models import User#Register API
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from django.db.models import Q
from django.db.models.functions import Concat, Replace
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

import time




@method_decorator(csrf_exempt, name='dispatch')
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
    
        })

class LoginView(APIView):
    permission_classes = (AllowAny, )
    login_serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = self.login_serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.login()
            print("<><><><><>< 40 ><><><><><><>",user)

            token = RefreshToken.for_user(user)
            print("<><><><><><> token <><><><><>",token)
            jwt_access_token_lifetime =  settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] # .SIMPLE_JWT.ACCESS_TOKEN_LIFETIME
            jwt_refresh_token_lifetime =  settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] # .SIMPLE_JWT.ACCESS_TOKEN_LIFETIME
            data = {
            "refresh": str(token),
            "access": str(token.access_token),
            "access_token_life_time_in_seconds" : jwt_access_token_lifetime.total_seconds(),
            "refresh_token_life_time_in_seconds" : jwt_refresh_token_lifetime.total_seconds(),
            "email":user.email,
            "username":user.username
            } 
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message":"error"})
    
# class SearchView(viewsets.ReadOnlyModelViewSet):
#     queryset = DeviceCircuitSubnets.objects.all()
#     serializer_class = SubnetDetailsSerializer
#     permission_classes = (IsAdminUser,)
#     filter_class = DeviceCircuitSubnets
#     filter_backends = (filters.SearchFilter,)
#     search_fields = (
#         'username',
#         'email'
#     )

#     def get_queryset(self):
#         return (
#             super().get_queryset()
#             .select_related('circuit','subnet','device')
#             .annotate(
#                 safe_subnet=Concat(
#                     F('subnet__subnet'),
#                     Replace(F('subnet__mask'), V('/'), V('_')),
#                     output_field=CharField()
#                 )
#             )
#         )

class SearchAPIView(APIView):
    
    def get(self,request):
        
        keyword = request.GET.get("search")
        user = User.objects.filter(Q(email=keyword) | Q(username=keyword)).first()
        if user:
            serializer_class = UserSerializer(user)
            return Response(serializer_class.data)
        else:
            return Response({'msg':'Not Found'})
        
        
        
class EmailViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
    def post(self, request):
        data = request.data
        print(" ---------email-----------",list(data.values()))
        all_email = list(data.values())
        for x in all_email:
            print("**************", x)
            message = f'Hello {x}!! Welcome.'
            print('<><><><><><><message=======',message)
            subject= 'Welcome To App'
            email_from = EMAIL_HOST_USER
            recipient_list = x
          #  fail_silently=False
            print("><><><><><><><>recipient><><><><><>",recipient_list)
           # print("--------email_from-------------",email_from)    
            send_mail(subject, message, email_from, [recipient_list],fail_silently=True)
            # time .sleep(15)
           # [r.email for r in recipient_list]
            #print("------------send_mail--------------")
        return Response({'msg':' Email sent'})
            
                    
    #     email = send_mail(
    #         'Title',
    #         (UserSerializer.name, UserSerializer.email, UserSerializer.username),
    #         'my-email',
    #         ['my-receive-email']
    #     )
    # #  email.attach_file(UserSerializer.file)
    #     email.send()
        

