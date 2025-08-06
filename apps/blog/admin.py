
from django.contrib import admin
from .models import Categoria_blog, Articulo

# Register your models here.

@admin.register(Categoria_blog)
class CategoriaBlogAdmin(admin.ModelAdmin):

    list_display = ('nombre', 'descripcion', 'id_categoria')
    search_fields = ('nombre',) 
    list_filter = ('nombre',) 


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'autor', 'categoria', 'fecha_publicacion', 'activo')
    list_filter = ('activo', 'categoria', 'autor', 'fecha_publicacion')
    search_fields = ('titulo', 'subtitulo', 'contenido', 'autor__username', 'categoria__nombre')
    date_hierarchy = 'fecha_publicacion' # Permite navegar por fecha de publicación
    ordering = ('-fecha_publicacion',) 
    raw_id_fields = ('autor', 'categoria') # Para campos ForeignKey, mejora la UX en el admin
    fieldsets = (
        (None, {
            'fields': ('titulo', 'subtitulo', 'contenido', 'imagen_principal', 'imagen_url')
        }),
        ('Información Adicional', {
            'fields': ('autor', 'categoria', 'fecha_publicacion', 'activo'),
            'classes': ('collapse',) # Opcional: hace que esta sección sea colapsable
        }), 
    )
