from reviews.serializers import ReviewSerializer
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ReviewGet(APIView):
    @swagger_auto_schema(
        operation_summary="Get all reviews",
        operation_description="Lista todas reviews",
        responses={200: ReviewSerializer.Review(many=True)}
    )
    def get(self, request):
        reviews = Review.objects.all().order_by('id')
        serializer = ReviewSerializer.Review(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReviewView(APIView):
    @swagger_auto_schema(
        operation_summary="Create Review",
        operation_description="Creates new review",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "product" : openapi.Schema(description="Produto que está sendo avaliado", type=openapi.TYPE_STRING),
                "content" : openapi.Schema(description="Avaliação do autor", type=openapi.TYPE_STRING),
                "brand" : openapi.Schema(description="Marca do produto", type=openapi.TYPE_STRING),
<<<<<<< HEAD
                "author" : openapi.Schema(description="Nome de usuário do autor da avaliação", type=openapi.TYPE_STRING),
=======
                "author" : openapi.Schema(description="Nome de usuário do autor da avaliação", type=openapi.TYPE_OBJECT),
>>>>>>> 41efcbc8d05391d642fc099b0ee2eb8d8d9de89c
                "product_url" : openapi.Schema(description="Link para a página do produto", type=openapi.TYPE_STRING),
                "score" : openapi.Schema(description="Nota dada pelo usuário", type=openapi.TYPE_INTEGER)
            }
        ),
        responses={201: ReviewSerializer.Review()},
    )
    def post(self, request):
        serializer = ReviewSerializer.Review(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            operation_summary = "Deletar Resenha",
            operation_description='Remove uma Resenha',
            responses={
                204: ReviewSerializer.Review(),
                404: None,
            },
    )
    def delete(self, request, pk=None):
        try:
            resenha = Review.objects.get(id=pk)
            resenha.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({'error': 'No Review found'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        operation_summary="Updates review", operation_description="Atualiza as informações de uma resenha",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "product" : openapi.Schema(description="Produto que está sendo avaliado", type=openapi.TYPE_STRING),
                "content" : openapi.Schema(description="Avaliação do autor", type=openapi.TYPE_STRING),
                "brand" : openapi.Schema(description="Marca do produto", type=openapi.TYPE_STRING),
                "author" : openapi.Schema(description="Nome de usuário do autor da avaliação", type=openapi.TYPE_STRING),
                "product_url" : openapi.Schema(description="Link para a página do produto", type=openapi.TYPE_STRING),
                "score" : openapi.Schema(description="Nota dada pelo usuário", type=openapi.TYPE_INTEGER)
            }
        ),
        responses={200:ReviewSerializer.Review(), 
                    400:ReviewSerializer.Review()},
    )
    def put(self, request, pk):
        rev = Review.objects.get(pk=pk)
        serializer = ReviewSerializer.Review(rev, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewGetOne(APIView):
    @swagger_auto_schema(
    operation_summary="Get one review",
    operation_description="Lista uma review pela id",
    responses={200: ReviewSerializer.Review(many=True)}
    )
    def get(self, request, pk):
        reviews = Review.objects.get(pk = pk)
        serializer = ReviewSerializer.Review(reviews)
        return Response(serializer.data, status=status.HTTP_200_OK)