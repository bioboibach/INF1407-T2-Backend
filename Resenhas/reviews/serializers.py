from rest_framework import serializers
from .models import Review

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'