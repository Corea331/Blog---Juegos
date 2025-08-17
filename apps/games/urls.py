from django.urls import path
from .views import JuegoCreateView, JuegoListView, JuegoDetailView, JuegoUpdateView, JuegoDeleteView, ComentarioJuegoCreateView, ComentarioJuegoUpdateView, ComentarioJuegoDeleteView, aprobar_comentario, PuntuarJuegoView

app_name = 'apps.games'

urlpatterns = [
    path('', JuegoListView.as_view(), name='lista_juegos'),
    path('<int:pk>', JuegoDetailView.as_view(), name='detalle_juego'),
    path('crear/', JuegoCreateView.as_view(), name='agregar_juego'),
    path('<int:pk>/editar', JuegoUpdateView.as_view(), name='editar_juego'),
    path('<int:pk>/eliminar', JuegoDeleteView.as_view(), name='eliminar_juego'),

    #=====Puntuación
    path('<int:pk>/puntuar', PuntuarJuegoView.as_view(), name='puntuar_juego'),

    #=======comentarios
    path('<int:juego_id>/comentar', ComentarioJuegoCreateView.as_view(), name='agregar_comentario'),
    path('comentario/<int:pk>/editar', ComentarioJuegoUpdateView.as_view(), name='editar_comentario'),
    path('comentario/<int:pk>/eliminar', ComentarioJuegoDeleteView.as_view(), name='eliminar_comentario'),
    path('comentario/<int:pk>/aprobar', aprobar_comentario, name='aprobar_comentario')
]