from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Importamos el modelo de Usuario de Django
from django.conf import settings

# Create your models here.

class Plataforma(models.Model):#id_plataforma se crea automáticamente como 'id' (AutoField) en Django
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre de la Plataforma")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Plataforma"
        verbose_name_plural = "Plataformas"
        ordering = ['nombre'] # Ordenar por nombre por defecto

    def __str__(self):
        return self.nombre
    

class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del Género")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
        ordering = ['nombre'] # Ordenar por nombre por defecto

    def __str__(self):
        return self.nombre

    
class Juego(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título del Juego")
    descripcion = models.TextField(verbose_name="Descripción Completa")
    fecha_lanzamiento = models.DateField(verbose_name="Fecha de Lanzamiento")
    desarrollador = models.CharField(max_length=100, null=True, blank=True, verbose_name="Desarrollador")
    editor = models.CharField(max_length=100, null=True, blank=True, verbose_name="Editor")
    imagen_portada = models.ImageField(
        upload_to='juegos/portadas/', # Los archivos se guardarán en MEDIA_ROOT/juegos/portadas/
        null=True,
        blank=True,
        verbose_name="Imagen de Portada"
    )
    video_trailer_url = models.URLField(null=True, blank=True, verbose_name="URL del Trailer")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_agregado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Agregado")
    agregado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Agregado por"
    )
    
    # Relaciones Muchos a Muchos (Django crea tablas intermedias automáticamente)
    plataformas = models.ManyToManyField(Plataforma, related_name='juegos', verbose_name="Plataformas")
    generos = models.ManyToManyField(Genero, related_name='juegos', verbose_name="Géneros")
    
    # Campo para almacenar el promedio de puntuación (se actualizará con lógica posterior)
    promedio_puntuacion = models.DecimalField(
        max_digits=3, 
        decimal_places=2,
        default=0.00,
        verbose_name="Puntuación Promedio"
    )

    class Meta:
        verbose_name = "Juego"
        verbose_name_plural = "Juegos"
        ordering = ['titulo'] # Ordenar por título por defecto

    def __str__(self):
        return self.titulo

    
class Puntuacion(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, verbose_name="Juego")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name="Usuario"
    )
    valor = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], # Puntuación de 1 a 5
        verbose_name="Valor de la Puntuación"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        verbose_name = "Puntuación"
        verbose_name_plural = "Puntuaciones"
        unique_together = ('juego', 'usuario')#Un usuario solo puede puntuar un juego una vez
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.username} puntuó {self.juego.titulo} con {self.valor}"


class Comentario(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, verbose_name="Juego")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Usuario"
    )
    texto = models.TextField(verbose_name="Comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    aprobado = models.BooleanField(default=False, verbose_name="Aprobado para Publicación")

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-fecha_creacion'] 

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.juego.titulo}"
    