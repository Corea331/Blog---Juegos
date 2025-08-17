from django.views.generic import TemplateView
from django.shortcuts import render
from apps.blog.models import Articulo
from apps.games.models import Juego
from django.db.models import Count

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ultimos_juegos'] = Juego.objects.all().order_by('-fecha_lanzamiento')[:5]

        context['articulos_destacados'] = Articulo.objects.filter(activo=True).annotate(num_comentarios=Count('comentarios')).order_by('-num_comentarios')[:3]

        context['juegos_destacados'] = Juego.objects.filter(activo=True, promedio_puntuacion__gt=0).annotate(num_comentarios=Count('comentarios')).order_by('-promedio_puntuacion', '-num_comentarios')[:3]

        context['ultimos_articulos'] = Articulo.objects.filter(activo=True, fecha_publicacion__isnull=False).order_by('-fecha_publicacion')[:4]

        return context

def sobre_nosotros(request):
    return render(request, 'nosotros.html')