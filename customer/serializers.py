from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import Profile


User = get_user_model()

class UserRegisterApiView(serializers.Serializer):
    class Meta:
        model = User
        fields = "__all__"

class UserRegisterSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64,read_only=True)
    phone_number = serializers.CharField(max_length=13)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=200,write_only=True)
    password2 = serializers.CharField(max_length=200,write_only=True)

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number',None)
        username = validated_data.pop('username',None)
        password = validated_data.pop('password',None)
        password2 = validated_data.pop('password2',None)

        if password!=password2:
            raise serializers.ValidationError({"message":"password not matched"})
        if User.objects.filter(phone_number=phone_number).count()>0:
            raise serializers.ValidationError({"message":"Phone number already exist"})
        if User.objects.filter(username=username).count()>0:
            raise serializers.ValidationError({"message":"Username already exist"})
        user = User(phone_number=phone_number,username=username,**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13,write_only=True)
    token = serializers.CharField(max_length=64,read_only=True)
    password = serializers.CharField(max_length=200,write_only=True)
    
    def validate(self, attrs):
        phone_number = attrs.get("phone_number",None)
        password = attrs.get("password",None)
        user = authenticate(phone_number=phone_number,password=password)
        if user is None:
            raise serializers.ValidationError({"message":"phone number or password error"})
        return user

class ProfileModelSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"
    