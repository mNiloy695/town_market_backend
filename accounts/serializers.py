from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import get_user_model

User=get_user_model()


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True,required=False, allow_blank=True)
    class Meta:
        model=User
        fields=['username','email','password','phone','user_type','first_name','last_name','confirm_password']
    
   
    def validate(self, attrs):
        password=attrs.get('password',None)
        confirm_password=attrs.pop('confirm_password',None)
        email=attrs.get('email',None)

        if password:
            if password != confirm_password:
               raise serializers.ValidationError("Password and Confirm Password does not match")
        if email: 
            if email and User.objects.filter(email=email).exclude(id=self.instance.id if self.instance else None).exists():
              raise serializers.ValidationError({'email':"Email is already exist"})
        return attrs
    
    # for hasing password while creating user
    def create(self,validated_data):
        password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    # for hasing password while updating user
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)
    