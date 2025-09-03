from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import PerfilUpdateView

app_name = 'usuarios'

urlpatterns = [
    # Vista para actualizar el perfil del usuario logueado
    path('perfil/', PerfilUpdateView.as_view(), name='perfil'),
    
    # URLs para el cambio de contraseña
    path('cambiar-contrasena/', auth_views.PasswordChangeView.as_view(template_name='usuarios/cambiar_contrasena.html', success_url=reverse_lazy('usuarios:password_change_done')), name='password_change'),
    path('cambiar-contrasena/hecho/', auth_views.PasswordChangeDoneView.as_view(template_name='usuarios/password_change_done.html'), name='password_change_done'),

    # URLs para la recuperación de contraseña (Olvidaste tu contraseña)
    path('recuperar-contrasena/', auth_views.PasswordResetView.as_view(template_name='usuarios/recuperar_contrasena.html', email_template_name='usuarios/password_reset_email.html'), name='password_reset'),
    path('recuperar-contrasena/hecho/', auth_views.PasswordResetDoneView.as_view(template_name='usuarios/recuperar_contrasena_hecho.html'), name='password_reset_done'),
    path('recuperar-contrasena/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/recuperar_contrasena_confirmar.html'), name='password_reset_confirm'),
    path('recuperar-contrasena/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/recuperar_contrasena_completo.html'), name='password_reset_complete'),
]