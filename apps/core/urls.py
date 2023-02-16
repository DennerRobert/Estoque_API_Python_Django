from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from apps.core.views import CadastroUsuarioView, index
from django.contrib.auth import views as auth_views

urlpatterns = [
     # path('', index, name="index"),

    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', CadastroUsuarioView.as_view(), name='cadastro'),
]
