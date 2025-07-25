# Generated by Django 4.2.20 on 2025-07-08 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_pago', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidoitem',
            name='producto',
        ),
        migrations.AddField(
            model_name='pedidoitem',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pedidoitem',
            name='imagen_url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidoitem',
            name='nombre',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidoitem',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidoitem',
            name='producto_id_externo',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
