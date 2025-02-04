# Generated by Django 5.1.2 on 2025-02-04 12:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='nombre')),
                ('last_name', models.CharField(max_length=100, verbose_name='apellido')),
                ('telephone_number', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Ingrese un número de teléfono válido.', regex='^\\+?\\d{1,3}?[-.\\s]?\\(?\\d{1,4}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}$')], verbose_name='nº de teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email')),
                ('color', models.CharField(default='#3498db', max_length=7, verbose_name='color')),
                ('services', models.ManyToManyField(blank=True, related_name='employees', to='service.service', verbose_name='servicios realizados')),
            ],
            options={
                'verbose_name': 'empleado',
                'ordering': ['first_name', 'last_name'],
            },
        ),
    ]
