# Generated by Django 5.1.7 on 2025-03-23 14:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Wishlist',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('email', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('country', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('state', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customer Address',
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('New Order', 'New Order'), ('Item Shipped', 'Item Shipped'), ('Item Delivered', 'Item Delivered')], default=None, max_length=100)),
                ('seen', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notification',
            },
        ),
    ]
