from django.db import models
from django.dispatch import receiver
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete

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
    desarrollador = models.CharField(max_length=100, null=True, blank=True)
    editor = models.CharField(max_length=100, null=True, blank=True)
    imagen_portada = models.ImageField(
        upload_to='juegos/portadas/', # Los archivos se guardarán en MEDIA_ROOT/juegos/portadas/
        null=True,
        blank=True,
        verbose_name="Imagen de Portada"
    )
    video_trailer_url = models.URLField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    agregado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Relaciones Muchos a Muchos (Django crea tablas intermedias automáticamente)
    plataformas = models.ManyToManyField(Plataforma, related_name='juegos')
    generos = models.ManyToManyField(Genero, related_name='juegos')

    # Campo para almacenar el promedio de puntuación (se actualizará con lógica posterior)
    promedio_puntuacion = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    class Meta:
        verbose_name = "Juego"
        verbose_name_plural = "Juegos"
        ordering = ['titulo'] # Ordenar por título por defecto

    def __str__(self):
        return self.titulo


class Puntuacion(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='puntuaciones')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'puntuaciones'
    )
    valor = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], # Puntuación de 1 a 5
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('juego', 'usuario')#Un usuario solo puede puntuar un juego una vez
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.username} puntuó {self.juego.titulo} con {self.valor}"


class ComentarioJuego(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_creacion']
        permissions = [('aprobar_comentario', 'Puede aprobar comentarios')]

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.juego.titulo}"

@receiver([post_save, post_delete], sender=Puntuacion)
def actualizar_promedio(sender, instance, **kwargs):
    juego = instance.juego
    promedio = juego.puntuaciones.aggregate(avg_puntuacion=Avg('valor'))['avg_puntuacion'] or 0.00
    juego.promedio_puntuacion = round(promedio, 2)
    juego.save(update_fields=['promedio_puntuacion'])