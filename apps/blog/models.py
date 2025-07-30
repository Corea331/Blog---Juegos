from django.db import models
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
    imagen_principal = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Imagen Principal")

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
        blank=True,
        related_name='articulos', # Nombre inverso para acceder desde Categoria_blog
        verbose_name="Categoría"
    )

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['-fecha_publicacion', '-fecha_creacion'] # Ordenar por fecha de publicación descendente

    def __str__(self):
        return self.titulo



