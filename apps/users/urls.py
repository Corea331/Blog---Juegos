from django.urls import path, include
from .views import RegisterUserView, UpdateUserView, UserListView, UserDetailView, ProfileView, DeleteUserView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'apps.users'

urlpatterns = [
    path('signup/', RegisterUserView.as_view(template_name='account/signup.html'), name='signup'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('profile/', ProfileView.as_view(), name="profile"),
    #path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('update_user/<int:pk>', UpdateUserView.as_view(), name='update_user'),
    path('delete_user/<int:pk>', DeleteUserView.as_view(), name='delete_user'),
    path('list_users', UserListView.as_view(), name='list_users'),
    path('detail_user/<int:pk>', UserDetailView.as_view(), name='detail_user'),
    path('', include('allauth.urls')),
]