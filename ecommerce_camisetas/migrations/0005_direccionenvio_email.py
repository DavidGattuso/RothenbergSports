# Generated by Django 3.1 on 2024-10-26 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_camisetas', '0004_carritoitem_talla'),
    ]

    operations = [
        migrations.AddField(
            model_name='direccionenvio',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
