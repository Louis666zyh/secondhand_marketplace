# Generated by Django 4.2 on 2025-03-16 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_available_until'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='location',
            field=models.CharField(blank=True, help_text='Location of the product.', max_length=255, null=True),
        ),
    ]
