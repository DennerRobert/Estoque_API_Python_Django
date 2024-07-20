import random
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque.settings')
django.setup()

from apps.produto.models import Products

products = ["Laptop", "Smartphone", "Tablet", "Printer", "Monitor", "Keyboard", "Mouse", 
			"Headphones", "External Hard Drive", "USB Flash Drive", "Webcam", "Router", 
			"Network Switch", "Desk Chair", "Office Desk", "Desk Lamp", "Printer Paper", 
			"Ink Cartridge", "Charging Cable", "Power Bank", "Speakers", "Graphics Card", 
			"Motherboard", "Processor", "RAM", "Solid State Drive (SSD)", "Hard Disk Drive (HDD)", 
			"Surge Protector", "Docking Station", "Projector"]


def add_products():
	"""
		Iterates through a list of products, 
		generates random quantity and price 
		values for each product, and creates
		a new Products object for each product
		with the generated values.
	"""
	for name in products:
		quantity = random.randint(10, 100)
		price = round(random.uniform(10.0, 100.0), 2)

		product = Products.objects.create(
			product=name,
			price=price,
			inventory=quantity,
		)
		print(f"Product '{product.product}' added successfully.")

if __name__ == '__main__':
	add_products()
