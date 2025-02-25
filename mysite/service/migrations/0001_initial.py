# Generated by Django 5.1.2 on 2025-02-04 12:33

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('color', models.CharField(default='#ffffff', max_length=7, verbose_name='color')),
            ],
            options={
                'verbose_name': 'categoría',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('duration', models.DurationField(blank=True, help_text='Duración del servicio', null=True, verbose_name='duración')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='precio')),
                ('available', models.CharField(blank=True, choices=[('SI', 'Sí'), ('NO', 'No')], default='SI', max_length=2, null=True, verbose_name='disponibiidad')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='service.category', verbose_name='categoría')),
            ],
            options={
                'verbose_name': 'servicio',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='nombre del bono')),
                ('total_sessions', models.PositiveIntegerField(verbose_name='número de sesiones')),
                ('price_session', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='precio sesión')),
                ('discount', models.IntegerField(default=0, help_text='Ingrese un valor entre 0 y 100', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='descuento (%)')),
                ('discounted_price', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=8, verbose_name='precio con descuento')),
                ('services', models.ManyToManyField(related_name='vouchers', to='service.service', verbose_name='servicios')),
            ],
            options={
                'verbose_name': 'bono',
                'ordering': ['name'],
            },
        ),
    ]
