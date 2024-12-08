"""
URL configuration for Resenhas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reviews import views as rev_view
from accounts import views as acc_view
from rest_framework import routers, permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi

schema_view = yasg_schema_view(
    openapi.Info(
        title = "Resenha Swagger API",
        default_version = 'v1',
        description = "Documentação do Projeto - Resenhas",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('docs/', include_docs_urls(title='Documentação da API')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger-ui'),
    path('api/v1/', include(routers.DefaultRouter().urls)),
    path('openapi', get_schema_view(title="ResenhAPI", description="API para obter Resenhas",), name='openapi-schema'),

    path('api/accounts/token-auth/', acc_view.CustomAuthToken.as_view(), name='token-auth'),
    path('api/accounts/create-user/', acc_view.CreateUserView.as_view(), name='create-user'),

    path('api/resenhas/', rev_view.ReviewGetView.as_view(), name='resenha-list'),
    path('api/resenhas/post/', rev_view.ReviewPostView.as_view(), name='resenha-post'),
    path('api/resenhas/delete/<int:pk>/', rev_view.ReviewDeleteView.as_view(), name='resenha-delete'),
    path('api/resenhas/update/<int:pk>/', rev_view.ReviewPutView.as_view(), name='resenha-update'),
    path('api/resenhas/<int:pk>/', rev_view.ReviewGetOne.as_view(), name='resenha-getone'),
]