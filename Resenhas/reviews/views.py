### AFTER ###
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Review
from .serializers import Serializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ReView(APIView):
    '''
    CRUD
    '''

    @swagger_auto_schema (
        operation_summary = 'Get Resenhas',
        operation_description = "Lista todas as resenhas",
        responses={200: Serializer(many=True)}
    )
    def get(self, request):
        queryset = Review.objects.all().order_by('name')
        serializer = Serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary = "Nova Resenha",
        operation_description = "Cria nova resenha",
        request_body = Serializer,
        responses = {201: Serializer}
    )
    def post(self, request):
        serializer = Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
