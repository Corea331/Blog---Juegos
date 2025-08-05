from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .forms import RegisterUserForm
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterUser(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm

    def form_valid(self, form):
        messages.success(self.request, 'Registro de usuario exitoso. Por favor iniciar sesión.')
        form.save()

        return redirect('apps.users:register')

class LoginUser(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Login exitoso.')

        return reverse('apps.users:login')


class LogoutUser(LogoutView):
    template_name = 'registration/logout.html'

    def get_success_url(self):
        messages.success(self.request, 'Logout exitoso.')

        return reverse('apps.users:logout')
    
#Agrego vista para el perfil
class ProfileView(LoginRequiredMixin, TemplateView):
    #LoginRequiredMixin asegura que solo los usuarios autenticados puedan acceder a esta vista.
    template_name = 'users/profile.html'