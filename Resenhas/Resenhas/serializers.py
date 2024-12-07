from rest_framework import serializers
from reviews.models import Review

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review # nome do modelo
        fields = '__all__' # lista de campos