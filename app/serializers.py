from rest_framework import serializers
from .models import *
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usercustome
        fields = ['id','username', 'phone_number', 'password','user_role','email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usercustome(
            # id=validated_data['id'],
            username=validated_data['username'],
            user_role=validated_data['user_role'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user    
    
    
class UserLimitedUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usercustome
        fields = ['username', 'email', 'user_role','phone_number']  # Only allow these fields to update


