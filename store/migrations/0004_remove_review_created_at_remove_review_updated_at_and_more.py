# Generated by Django 5.1.6 on 2025-03-22 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_merge_20250318_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='review',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveBigIntegerField(default=3),
        ),
    ]
