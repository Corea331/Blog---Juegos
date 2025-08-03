from django.views.generic import ListView, DetailView
from .models import Articulo 

class ArticuloListView(ListView):
    """
    CBV para listar todos los artículos del blog pero como una preview, el usuario tiene que seleccionar y ahi se abre el detalle con la vista ArticulosDetailView que esta abajo
    """
    model = Articulo # Modelo que voy a listar
    template_name = 'blog/articulo_list.html'
    context_object_name = 'articulos' #Variable donde va la lista del queryset

    def get_queryset(self):
        """
        Sobrescribe el queryset para filtrar solo artículos activos
        y ordenarlos por fecha de publicación descendente.
        """
        return Articulo.objects.filter(activo=True).order_by('-fecha_publicacion', '-fecha_creacion')
    

class ArticuloDetailView(DetailView):
    """
    CBV para mostrar el detalle del articulo cuando el usuario hace click
    """
    model = Articulo 
    template_name = 'blog/articulo_detail.html'
    # El nombre de la variable por defecto que se pasa a la plantilla es 'object' o 'articulo'

    def get_queryset(self):
        return Articulo.objects.filter(activo=True)
