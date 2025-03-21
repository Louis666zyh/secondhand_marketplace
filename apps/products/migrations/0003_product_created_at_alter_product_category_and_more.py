# Generated by Django 4.2 on 2025-03-14 01:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 3, 14, 9, 12, 45, 900041), help_text='Timestamp when the product was created.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(help_text='Category of the product.', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('reserved', 'Reserved'), ('sold', 'Sold')], default='available', help_text='Current status of the product.', max_length=20),
        ),
    ]
