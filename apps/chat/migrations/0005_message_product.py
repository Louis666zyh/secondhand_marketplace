# Generated by Django 4.2 on 2025-03-19 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_location'),
        ('chat', '0004_remove_message_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='product',
            field=models.ForeignKey(blank=True, help_text='Product associated with this message (optional).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product'),
        ),
    ]
