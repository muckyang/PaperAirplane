from rest_framework import serializers
from .models import Custom

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom
        fields = '__all__'