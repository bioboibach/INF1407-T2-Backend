from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status


class CreateUserView(APIView):
    '''
    View para POST, criar um novo usuário
    '''
    @swagger_auto_schema(
        operation_summary='Cria User',
        operation_description='Cria um User na base de dados e retorna o Objeto User do usuario criado caso bem sucedido',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password', 'email'],
        ),
        responses={
            status.HTTP_201_CREATED: 'User created',
            status.HTTP_400_BAD_REQUEST: 'Error: Bad request',
        },
    )
    def post(self, request):
        '''
        Input: request um objeto representando o pedido HTTP
        
        Output: Objeto User (JSON) caso a função seja bem sucedida

        Depende de:
        - APIView
        - UserSerializer
        - Response
        '''
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status.HTTP_400_BAD_REQUEST)  

class CustomAuthToken(ObtainAuthToken):
    '''
    View:
    - GET de um Authenticator Token
    - POST um Objeto User na base de dados
    - DELETE o Authenticator Token especificado
    '''
    @swagger_auto_schema(
        operation_summary = 'Encontra User a partir do Token',
        operation_description = "Retorna a string 'username' do User caso seja um usuário logado, retorna 'GuestUser' caso não seja autenticado",
        security=[{'Token':[]}],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Type in the Authenticator Token',
            ),
        ],
        responses={
            200: openapi.Response(
            description='Nome do usuário',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'username': openapi.Schema(type=openapi.TYPE_STRING)},
               ),
            )
        }
    )
    def get(self, request):
        '''
        Input: request um objeto representando o pedido HTTP
        
        Output: retorna o username caso seja um usuário, retorna 'GuestUser' caso não seja autenticado

        Depende de:
        - Token
        - APIView
        - Response
        '''
        try:
            token_obj = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION'))
            user = token_obj.user
            return Response({'username': user.username},status=status.HTTP_200_OK)
        except (Token.DoesNotExist, AttributeError):
            return Response({'username': 'GuestUser'},status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary='Get token pelo login',
        operation_description='Retorna o Authenticator Token depois do login do usuário',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password'],
        ),
        responses={
            status.HTTP_200_OK: 'Token is returned.',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized request.',
        },  
    )
    def post(self, request, *args, **kwargs):
        '''
        Input: 
        - request um objeto representando o pedido HTTP
        - lista de argumentos contendo username e password
        
        Output: Objeto User (JSON) caso a função seja bem sucedida

        Depende de:
        - Token
        - APIView
        - Response
        '''
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({'token': token.key})
        
    @swagger_auto_schema(
        operation_summary='Logout do User',
        operation_description='Faz logout do User baseado no Authenticator Token atual',
        security=[{'Token':[]}],
        manual_parameters=[
            openapi.Parameter('Authorization',
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Type in the Authenticator Token',
            ),
        ],
        responses={
            status.HTTP_200_OK: 'User logged out',
            status.HTTP_400_BAD_REQUEST: 'Bad request',
            status.HTTP_401_UNAUTHORIZED: 'User not authenticated',
            status.HTTP_403_FORBIDDEN: 'User not authorized to logout',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Server Error',
        },
    )
    def delete(self, request):
        '''
        Input: request um objeto representando o pedido HTTP
        
        Output: mensagem de logout

        Depende de:
        - Token
        - APIView
        - Response
        '''
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            token_obj = Token.objects.get(key=token)
        except (Token.DoesNotExist, IndexError):
            return Response({'msg': 'Token não existe.'}, status=status.HTTP_400_BAD_REQUEST)
        user = token_obj.user
        if user.is_authenticated:
            request.user = user
            logout(request)
            token = Token.objects.get(user=user)
            token.delete()
            return Response({'msg': 'User logged out'},status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'No User signed'},status=status.HTTP_403_FORBIDDEN) 




