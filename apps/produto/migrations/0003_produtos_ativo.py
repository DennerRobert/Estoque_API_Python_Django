# Generated by Django 3.2.16 on 2023-02-15 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_alter_produtos_estoque'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtos',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
