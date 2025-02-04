# Generated by Django 5.1.2 on 2025-02-04 12:33

import client.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='nombre')),
                ('last_name', models.CharField(max_length=100, verbose_name='apellido')),
                ('telephone_number', models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Ingrese un número de teléfono válido. Debe contener entre 9 y 15 dígitos.', regex='^\\d{9,15}$')], verbose_name='nº de teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email')),
            ],
            options={
                'verbose_name': 'cliente',
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='ClientVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField(default=django.utils.timezone.now, verbose_name='fecha de compra')),
                ('expiration_date', models.DateField(default=client.models.default_expiration_date, verbose_name='fecha de caducidad')),
                ('sessions_remaining', models.PositiveIntegerField(verbose_name='sesiones restantes')),
                ('is_active', models.BooleanField(choices=[(True, 'Sí'), (False, 'No')], default=True, verbose_name='estado')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='client.client', verbose_name='cliente')),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_voucher', to='service.voucher')),
            ],
            options={
                'verbose_name': 'bono del cliente',
                'ordering': ['voucher', 'purchase_date'],
            },
        ),
    ]
