# Generated by Django 5.1.1 on 2024-11-06 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashionapp', '0014_cart_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
