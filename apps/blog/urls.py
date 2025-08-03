
from django.urls import path
from .views import ArticuloListView, ArticuloDetailView

app_name = 'blog'

urlpatterns = [
    path('', ArticuloListView.as_view(), name='lista_articulos'), # URL para mostrar todos los articulos
    path('<int:pk>/', ArticuloDetailView.as_view(), name='detalle_articulo'),  # URL para mostrar el detalle de un artículo específico, Por ejemplo: /blog/5/
]