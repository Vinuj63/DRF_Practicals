from rest_framework import  serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password# Register serializer
from django.db.models import Q
from django.contrib import auth
# from                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         import 



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name','email')
        extra_kwargs = {
            'password':{'write_only': True},
        }
        
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   password=make_password(validated_data['password']),
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'],
                                   email=validated_data['email'])
        return user# User serializer


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()
    class Meta:
        model = User
        fields =  ['email']
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=5, max_length=64, write_only=True, required=True)
    password = serializers.CharField(min_length=6, max_length=64, write_only=True, required=True)
        
    def login(self, **kwargs):

        username = self.validated_data['username']
        password = self.validated_data['password']

        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        if not user:
            raise serializers.ValidationError({"message": ["No active account found with the given credentials."]})

        user = auth.authenticate(username=user.username, password=password)

        if not user:
            raise serializers.ValidationError({"message": ["No active account found with the given credentials."]})
        return user