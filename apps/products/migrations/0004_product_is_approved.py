# Generated by Django 4.2 on 2025-03-15 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_created_at_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_approved',
            field=models.BooleanField(default=False, help_text='Indicates whether the product is approved by an admin.'),
        ),
    ]
