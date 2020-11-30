from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password", "gender", "bornyear")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
            first_name = "first",
            last_name = "last",
            gender=validated_data["gender"],
            bornyear=validated_data["bornyear"]
        )
        return user

# 접속 유지중인지 확인
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uid","username", "email", "password", "gender", "bornyear")

# 로그인
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("로그인 실패")

# 정보수정
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "gender", "bornyear"]

# 정보삭제
class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'