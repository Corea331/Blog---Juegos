from django.views.generic import ListView
from .models import Articulo 

class ArticuloListView(ListView):
    """
    Vista basada en clase para listar todos los artículos del blog.
    Muestra solo los artículos que están activos y los ordena por fecha de publicación.
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


