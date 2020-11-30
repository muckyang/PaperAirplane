from .models import Comment
from rest_framework import serializers
from django.contrib.auth import authenticate

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# 정보수정
class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["description", "score"]

# 정보삭제
class CommentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'