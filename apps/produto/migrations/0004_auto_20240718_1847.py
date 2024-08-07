# Generated by Django 3.2.16 on 2024-07-18 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque_produtos', '0003_auto_20240718_1847'),
        ('produto', '0003_produtos_ativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('product', models.CharField(max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='price')),
                ('inventory', models.IntegerField(default=0, verbose_name='current inventory')),
            ],
            options={
                'ordering': ('product',),
            },
        ),
        migrations.DeleteModel(
            name='Produtos',
        ),
    ]
