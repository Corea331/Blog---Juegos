from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from allauth.account.views import PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from apps.blog.models import ComentarioArticulo
from .forms import RegisterUserForm, CustomPasswordResetForm, UpdateUserForm
from .models import User


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'users/list_users.html'
    context_object_name = 'usuarios'
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.es_colaborador
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(is_superuser=False)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'usuario'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['articulos_count'] = user.articulos_publicados.count()
        context['comentarios_count'] = user.comentarioarticulo_set.count()
        return context


class RegisterUserView(CreateView):
    model = User
    template_name = 'account/signup.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')


class UpdateUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'account/update_user.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        user = self.get_object()
        return self.request.user.is_superuser or (self.request.user == user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)
    

class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'confirmar_eliminar.html'
    success_url = reverse_lazy('apps.users:list_users')

    def test_func(self):
        target_user = self.get_object()
        current_user = self.request.user
        if target_user.is_superuser:
            return current_user.is_superuser
        return current_user.is_superuser or current_user.es_colaborador

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_objeto'] = 'usuario'
        context['contenido_relacionado'] = {
            'artículos': self.object.articulos_publicados.count(),
            'comentarios': ComentarioArticulo.objects.filter(usuario=self.object).count()
        }
        return context


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'account/password_reset.html'
    success_message = 'Se ha enviado un correo con instrucciones para reestablecer su contraseña.'
    success_url = reverse_lazy('apps.users:login')

class ProfileView(LoginRequiredMixin, DetailView):
    #LoginRequiredMixin asegura que solo los usuarios autenticados puedan acceder a esta vista.
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['articulos_recientes'] = user.articulos_publicados.all()[:5]
        return context

    def get_object(self,):
        return self.request.user