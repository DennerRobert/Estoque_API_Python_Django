from django.db import models
from django.contrib.auth.models import User
from apps.core.models import TimeStempedModel
from apps.produto.models import Products

MOVEMENT = (
	('e', 'entry'),
	('s', 'exit'),
)

class Inventory(TimeStempedModel):
	employee = models.ForeignKey(User, on_delete=models.CASCADE)
	invoice_number = models.PositiveIntegerField('invoice number', null=True, blank=True)
	movement = models.CharField(max_length=1, choices=MOVEMENT)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return '{} - {}'.format(self.pk, self.created.strftime('%d-%m-%Y'))    

class InventoryItems(models.Model):
	inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
	product = models.ForeignKey(Products, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	balance = models.FloatField()


	class Meta:
		ordering = ('pk',)

	def __str__(self):
		return '{} - {} - {}'.format(self.pk, self.inventory.pk, self.product)
