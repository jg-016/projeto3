from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    PERFIL_ADMIN = 1
    PERFIL_USUARIO = 2
    PERFIL_CHOICES = [
        (PERFIL_ADMIN, 'Administrador'),
        (PERFIL_USUARIO, 'Usuário'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    perfil = models.IntegerField(choices=PERFIL_CHOICES, default=PERFIL_USUARIO)
    aniversario = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.usuario.username} ({self.get_perfil_display()})'
