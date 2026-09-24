from django.contrib.auth.models import User
from django.db import models

from .Produto import Produto


class Favorito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='favoritos')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.produto}'
