from django import forms
from .models import Estoque, EstoqueItens
from django.forms import formset_factory

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        filds = ('funcionario', 'nf', 'movimentacao')
        exclude = ('id',)

class EstoqueItensForm(forms.ModelForm):
    class Meta:
        model: EstoqueItens
        filds = ('produto', 'quantidade', 'saldo')
        exclude = ('id', 'estoque',)

EstoqueItensFormSet = forms.inlineformset_factory(
    Estoque,
    EstoqueItens,
    EstoqueItensForm,
    min_num=1,
    extra=0,    
    validate_min=True
)
