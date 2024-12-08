from rest_framework import serializers

from .models import *

class ReviewSerializer: 
    class Review(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = '__all__'