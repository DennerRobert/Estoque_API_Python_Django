from django.db import models
from django.contrib.auth.models import User
from apps.core.models import TimeStempedModel
from apps.produto.models import Produtos

MOVIMENTACAO = (
    ('e', 'entrada'),
    ('s', 'saida'),
)

class Estoque(TimeStempedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    nf = models.PositiveIntegerField('nota fiscal', null=True, blank=True)
    movimentacao = models.CharField(max_length=1, choices=MOVIMENTACAO)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} - {}'.format(self.pk, self.created.strftime('%d-%m-%Y'))    

class EstoqueItens(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    saldo = models.PositiveIntegerField()

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.estoque.pk, self.produto)
