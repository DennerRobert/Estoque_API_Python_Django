# Generated by Django 3.2.16 on 2024-07-18 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque_produtos', '0002_alter_estoqueitens_saldo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado em')),
                ('invoice_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='invoice number')),
                ('movement', models.CharField(choices=[('e', 'entry'), ('s', 'exit')], max_length=1)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='InventoryItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('balance', models.FloatField()),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque_produtos.inventory')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.RemoveField(
            model_name='estoqueitens',
            name='estoque',
        ),
        migrations.RemoveField(
            model_name='estoqueitens',
            name='produto',
        ),
        migrations.DeleteModel(
            name='Estoque',
        ),
        migrations.DeleteModel(
            name='EstoqueItens',
        ),
    ]
