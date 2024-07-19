from django import forms
from .models import Inventory, InventoryItems
from django.forms import formset_factory

class InventoryForm(forms.ModelForm):
	class Meta:
		model = Inventory
		fields = ('employee', 'invoice_number', 'movement')
		exclude = ( 'movement','employee')
		widgets = {
			'invoice_number': forms.TextInput(attrs={'placeholder':'99999999'}),
			'employee':forms.TextInput(attrs={'required':'False'})
		}

class InventoryItemsForm(forms.ModelForm):
	class Meta:
		model: InventoryItems
		filds = ('product', 'quantity', 'balance')
		exclude = ('id', 'inventory',)
		widgets = {
			'quantity': forms.TextInput(attrs={'placeholder':'0','required': 'required'}),
			'balance': forms.TextInput(attrs={'placeholder':'0,00'}),
		}
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields['product'].widget.attrs.update({'id': 'id_estoqueitens_set-0-produto'})

InventoryItemsFormSet = forms.inlineformset_factory(
	Inventory,
	InventoryItems,
	InventoryItemsForm,
	min_num=1,
	extra=0,    
	validate_min=True
)
