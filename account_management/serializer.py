from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def validate(self, attrs):
        if User.objects.filter(username__exact=attrs.get('username', '')).exists():
            raise serializers.ValidationError("This username already exists")
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        # user.is_active = False # it depends if you want to set is_active equals to False
        user.is_active = True
        user.save()
        return user
    
class SigninSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def validate(self , attrs):
        user = User.objects.filter(username=attrs.get('username', '')).first()
        if not user:
            raise serializers.ValidationError("This user doesnot exists")
        
        if not user.is_active:
            raise serializers.ValidationError("Please verify email first")
        
        return super().validate(attrs)
    
 