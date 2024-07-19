from django.db import models

class Products(models.Model):
	active = models.BooleanField(default=True)
	product = models.CharField(max_length=100, unique=True)
	price = models.DecimalField('price', max_digits=7, decimal_places=2)
	inventory = models.IntegerField('current inventory', default=0)


	class Meta:
		ordering = ('product',)

	def __str__(self):
		return self.product