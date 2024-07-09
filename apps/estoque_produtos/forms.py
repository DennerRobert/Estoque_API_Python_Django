from django import forms
from .models import Estoque, EstoqueItens
from django.forms import formset_factory

class EstoqueForm(forms.ModelForm):
	class Meta:
		model = Estoque
		fields = ('funcionario', 'nf', 'movimentacao')
		exclude = ('id', 'movimentacao','funcionario')
		widgets = {
			'nf': forms.TextInput(attrs={'placeholder':'99999999'}),
			'funcionario':forms.TextInput(attrs={'required':'False'})
		}

class EstoqueItensForm(forms.ModelForm):
	class Meta:
		model: EstoqueItens
		filds = ('produto', 'quantidade', 'saldo')
		exclude = ('id', 'estoque',)
		widgets = {
			'quantidade': forms.TextInput(attrs={'placeholder':'0','required': 'required'}),
			'saldo': forms.TextInput(attrs={'placeholder':'0,00'}),
		}

EstoqueItensFormSet = forms.inlineformset_factory(
	Estoque,
	EstoqueItens,
	EstoqueItensForm,
	min_num=1,
	extra=0,    
	validate_min=True
)
