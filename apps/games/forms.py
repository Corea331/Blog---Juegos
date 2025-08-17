from django import forms
from .models import ComentarioJuego, Puntuacion

class ComentarioJuegoForm(forms.ModelForm):

    class Meta:
        model = ComentarioJuego
        fields = ['texto']
        widgets = {
            'texto' : forms.Textarea(attrs={
                'rows' : 4,
                'placeholder' : 'Escribe tu comentario aquí...',
            })
        }

    def clean_texto(self):
        texto = self.cleaned_data.get('texto')
        if len(texto) < 10:
            raise forms.ValidationError("El comentario debe tener al menos 10 caracteres.")
        return texto


class PuntuarJuegoForm(forms.ModelForm):

    class Meta:
        model = Puntuacion
        fields = ['valor']
        widgets = {
            'valor': forms.Select(choices=[(i, f"{i} estrella{'s' if i != 1 else ''}") for i in range(1, 6)]),
        }


    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor not in range(1, 6):
            raise forms.ValidationError("La puntuación debe estar entre 1 y 5")
        return valor









