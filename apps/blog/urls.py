
from django.urls import path
from .views import ArticuloListView 

urlpatterns = [
    path('', ArticuloListView.as_view(), name='lista_articulos'),
]