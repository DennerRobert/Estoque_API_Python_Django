from django.db import models

class Produtos(models.Model):
    ativo = models.BooleanField(default=True)
    produto = models.CharField(max_length=100, unique=True)
    preco = models.DecimalField('preço', max_digits=7, decimal_places=2)
    estoque = models.IntegerField('estoque atual', default=0)

    class Meta:
        ordering = ('produto',)

    def __str__(self):
        return self.produto