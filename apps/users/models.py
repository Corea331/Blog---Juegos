from datetime import date
from PIL import Image
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
import io

# Create your models here.}
class User(AbstractUser):
    nombre = models.CharField(max_length=45, default='sin especificar')
    apellido = models.CharField(max_length=45, default='sin especificar')
    email = models.EmailField(null=False, unique=True)
    fecha_nacimiento = models.DateField(verbose_name='fecha nacimiento', default=date(2000, 1, 1))
    es_colaborador = models.BooleanField(verbose_name='es colaborador', default=False)
    imagen = models.ImageField(null=True, blank=True, upload_to='usuario/', default='usuario/user-default.jpg')

    def save(self, *args, **kwargs):
        if self.imagen and self.imagen.name != 'usuario/user-default.jpg':
            try:
                img = Image.open(self.imagen)
                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))

                output = io.BytesIO()
                img.save(output, format='JPEG', quality=85)
                output.seek(0)

                self.imagen.save(
                    self.imagen.name,
                    ContentFile(output.getvalue()),
                    save = False
                )
            except Exception as e:
                print(f'Error procesando la imagen: {e}')
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ('-date_joined', '-nombre')
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['nombre', 'apellido']),
        ]
        permissions = [
            ('es_colaborador', 'Puede editar y crear contenido'),
            ('puede_eliminar_usuario', 'Puede eliminar usuarios no superusuarios'),
        ]

    def clean(self):
        super().clean()

        self.email = self.email.lower().strip() if self.email else None

        if self.email and '@' not in self.email:
            raise ValidationError('Ingrese un email válido')

        if User.objects.filter(email__iexact=self.email).exclude(pk=self.pk).exists():
            raise ValidationError('Este email ya está registrado')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def get_absolute_url(self):
        return reverse('index')
