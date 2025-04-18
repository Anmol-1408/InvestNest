# Generated by Django 4.2.16 on 2025-04-17 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='equity',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='product',
            name='features',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='financial_projection',
            field=models.TextField(blank=True),
        ),
    ]
