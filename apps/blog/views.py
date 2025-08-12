from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Articulo, Categoria_blog, ComentarioArticulo
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .forms import ComentarioForm


class ArticuloListView(ListView):
    """
    CBV para listar todos los artículos del blog pero como una preview, el usuario tiene que seleccionar y ahi se abre el detalle con la vista ArticulosDetailView que esta abajo
    """
    model = Articulo # Modelo que voy a listar
    template_name = 'blog/articulo_list.html'
    context_object_name = 'articulos' #Variable donde va la lista del queryset
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_articulos'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        """
        Sobrescribe el queryset para filtrar solo artículos activos
        y ordenarlos por fecha de publicación descendente.
        """
        return Articulo.objects.filter(activo=True).order_by('-fecha_publicacion', '-fecha_creacion')


class ArticuloPorCategoriaView(ListView):
    model = Articulo # Modelo que voy a listar
    template_name = 'blog/articulo_list.html'
    paginate_by = 10

    def get_queryset(self):
        categoria = get_object_or_404(Categoria_blog, nombre=self.kwargs['categoria'])
        return Articulo.objects.filter(categoria=categoria, activo=True).order_by('-fecha_publicacion', '-fecha_creacion')


class ArticuloDetailView(DetailView):
    """
    CBV para mostrar el detalle del articulo cuando el usuario hace click
    """
    model = Articulo 
    template_name = 'blog/articulo_detail.html'
    # El nombre de la variable por defecto que se pasa a la plantilla es 'object' o 'articulo'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Artículo eliminado correctamente.')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria_blog.objects.all()
        context['comentario_form'] = ComentarioForm()
        context['comentarios'] = self.object.comentarios.filter(aprobado=True)
        return context


class ArticuloCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Articulo
    fields = ['titulo', 'subtitulo', 'contenido', 'categoria', 'imagen_principal', 'imagen_url' ]
    template_name = 'blog/articulo_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.es_colaborador
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, 'Artículo creado correctamente.')
        return super().form_valid(form)


class ArticuloUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articulo
    fields = ['titulo', 'subtitulo', 'contenido', 'categoria', 'imagen_principal', 'imagen_url' ]
    template_name = 'blog/articulo_form.html'

    def test_func(self):
        articulo = self.get_object()
        return self.request.user.is_superuser or (self.request.user.es_colaborador and articulo.autor == self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Artículo actualizado correctamente.')
        return super().form_valid(form)


class ArticuloDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articulo
    fields = ['titulo', 'subtitulo', 'contenido', 'categoria', 'imagen_principal', 'imagen_url' ]
    template_name = 'confirmar_eliminar.html'

    def test_func(self):
        articulo = self.get_object()
        return self.request.user.is_superuser or (self.request.user.es_colaborador and articulo.autor == self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_objeto'] = 'artículo'
        context['contenido_relacionado'] = {'comentarios' : self.object.comentarios.count()}
        return context


def aprobar_comentario(request, pk):
    comentario = get_object_or_404(ComentarioArticulo, pk=pk)
    if request.user.has_perm('blog.aprobar_comentario'):
        comentario.aprobado = True
        comentario.save()
        messages.success(request, 'Comentario aprobado.')
    else:
        messages.error(request, 'No tienes permisos para aprobar comentarios')
    return redirect('apps.blog:detalle_articulo', pk=comentario.articulo.pk)


class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = ComentarioArticulo
    form_class = ComentarioForm
    template_name = 'comentario_form.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.articulo_id = self.kwargs['articulo_id']
        if self.request.user.has_perm('blog.aprobar_comentario'):
            form.instance.aprobado = True
            messages.success(self.request, 'Comentario publicado.')
        else:
            messages.success(self.request, 'Comentario enviado para aprobaión.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('apps.blog:detalle_articulo', kwargs={'pk': self.kwargs['articulo_id']})


class ComentarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComentarioArticulo
    form_class = ComentarioForm
    template_name = 'comentario_form.html'

    def test_func(self):
        return self.get_object().puede_editar(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Comentario actualizado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('apps.blog:detalle_articulo', kwargs={'pk': self.object.articulo.pk})


class ComentarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ComentarioArticulo
    template_name = 'confirma_eliminar.html'

    def test_func(self):
        return self.get_object().puede_editar(self.request.user)
    
    def get_success_url(self):
        return reverse('apps.blog:detalle_articulo', kwargs={'pk': self.object.articulo.pk})