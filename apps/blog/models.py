from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Categoria_blog(models.Model):

    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría de Blog"
        verbose_name_plural = "Categorías de Blog"
        ordering = ['nombre'] # Ordenar por nombre por defecto

    def articulos_count(self):
        return self.articulos.count()

    def __str__(self):
        return self.nombre


class Articulo(models.Model):

    id_articulo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200, verbose_name="Título del Artículo")
    subtitulo = models.CharField(max_length=250, blank=True, null=True, verbose_name="Subtítulo")
    contenido = models.TextField(verbose_name="Contenido")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_publicacion = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Publicación")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articulos_publicados', # Nombre inverso para acceder desde User
        verbose_name="Autor"
    )

    categoria = models.ForeignKey(
        Categoria_blog,
        on_delete=models.SET_NULL, # Si la categoría se elimina, la categoría del artículo se establece en NULL
        null=True,
        blank=False,
        related_name='articulos', # Nombre inverso para acceder desde Categoria_blog
        verbose_name="Categoría"
    )

    # Campo para subir una imagen directamente
    imagen_principal = models.ImageField(
        upload_to='blog/imagenes',
        blank=True,
        null=True,
        verbose_name="Imagen Principal (Archivo)"
    )

    # Nuevo campo para almacenar una URL de imagen
    imagen_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Imagen Principal (URL)"
    )


    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['-fecha_publicacion', '-fecha_creacion'] # Ordenar por fecha de publicación descendente

    def otener_imagen(self):
        if self.imagen_principal:
            return self.imagen_principal.url
        return self.imagen_url or None

    def get_absolute_url(self):
        return reverse('apps.blog:detalle_articulo', kwargs={'pk': self.pk})

    def __str__(self):
        return self.titulo

class ComentarioArticulo(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, verbose_name="Articulo", related_name='comentarios')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Usuario"
    )
    texto = models.TextField(verbose_name="Comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_edicion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Edición")
    aprobado = models.BooleanField(default=False, verbose_name="Aprobado para Publicación")

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-fecha_creacion']
        permissions = [('aprobar_comentario', 'Puede aprobar comentarios')]

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.articulo.titulo}"

    def puede_editar(self, usuario):
        return usuario == self.usuario or usuario.es_colaborador or usuario.is_superuser

    def puede_eliminar(self, usuario):
        return self.puede_editar(usuario)


