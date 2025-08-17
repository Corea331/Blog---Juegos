
from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria_blog, Articulo, ComentarioArticulo

# Register your models here.

@admin.register(Categoria_blog)
class CategoriaBlogAdmin(admin.ModelAdmin):

    list_display = ('nombre', 'articulos_count', 'descripcion_corta')
    search_fields = ('nombre', 'descripcion')

    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + "..." if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

    def articulos_count(self, obj):
        return obj.articulos_count()
    articulos_count.short_description = 'Artículos'


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):

    list_display = ('titulo', 'autor_link', 'categoria_link', 'estado', 'fecha_publicacion', 'imagen_preview' )
    list_filter = ('activo', 'categoria', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido', 'autor__username')
    date_hierarchy = 'fecha_publicacion' # Permite navegar por fecha de publicación
    ordering = ('-fecha_publicacion',)
    raw_id_fields = ('autor', 'categoria') # Para campos ForeignKey, mejora la UX en el admin
    fieldsets = (
        ('Información', {
            'fields': ('titulo', 'subtitulo', 'contenido')
        }),
        ('Multimedia', {
            'fields': ('imagen_principal', 'imagen_url'),
        }),
        ('Clasificación', {
            'fields': ('categoria', 'autor')
        }),
        ('Publicación', {
            'fields': ('activo', 'fecha_publicacion')
        }),
    )

    def autor_link(self, obj):
        if obj.autor:
            return format_html('<a href="admin/auth/user/{}/change">{}</a>', obj.autor.id, obj.autor.username)
        return "-"
    autor_link.short_description = 'Autor'

    def categoria_link(self, obj):
        if obj.categoria:
            return format_html('<a href="admin/blog/categoria_blog/{}/change">{}</a>', obj.categoria.pk, obj.categoria.nombre)
        return "-"
    categoria_link.short_description = 'Categoría'

    def imagen_preview(self, obj):
        if obj.imagen_principal:
            return format_html('<img src="{}" style="max-height: 50px;">', obj.imagen_principal.url)
        return "-"
    imagen_preview.short_description = 'Vista previa'

    def estado(self, obj):
        return 'Publicado' if obj.activo else 'Borrador'
    estado.short_description = 'Estado'


@admin.register(ComentarioArticulo)
class ComentarioArticuloAdmin(admin.ModelAdmin):
    list_display = ('articulo_link', 'usuario_link', 'estado', 'fecha_creacion', 'texto_corto')
    list_filter = ('aprobado', 'fecha_creacion')
    search_fields = ('texto', 'usuario__username', 'articulo__titulo')
    actions = ['aprobar_comentarios', 'rechazar_comentarios']

    def articulo_link(self, obj):
        return format_html('<a href="/admin/blog/articulo/{}/change/">{}</a>', obj.articulo.pk, obj.articulo.titulo[:30])
    articulo_link.short_description = 'Artículo'

    def usuario_link(self, obj):
        return format_html('<a href="/admin/auth/user/{}/change/">{}</a>', obj.usuario.pk, obj.usuario.username)
    usuario_link.short_description = 'Usuario'

    def texto_corto(self, obj):
        return obj.texto[:50] + "..." if len(obj.texto) > 50 else obj.texto
    texto_corto.short_description = 'Comentario'

    def estado(self, obj):
        if obj.aprobado:
            return format_html('<span style="color: green;">✓ Aprobado</span>')
        return format_html('<span style="color: orange;">⏳ Pendiente</span>')
    estado.short_description = 'Estado'

    def aprobar_comentarios(self, request, queryset):
        queryset.update(aprobado=True)
        self.message_user(request, f"{queryset.count()} comentarios aprobados")
    aprobar_comentarios.short_description = "Aprobar comentarios seleccionados"

    def rechazar_comentarios(self, request, queryset):
        queryset.update(aprobado=False)
        self.message_user(request, f"{queryset.count()} comentarios rechazados")
    rechazar_comentarios.short_description = "Rechazar comentarios seleccionados"

