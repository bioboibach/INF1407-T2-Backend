from django.urls import path

from . import views

urlpatterns = [
    path("lista/", views.ReView.as_view(), name='lista-carros'),
    path('insert/', views.ReView.as_view(), name='um-carro'),
]