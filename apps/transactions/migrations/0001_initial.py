# Generated by Django 4.2 on 2025-03-12 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', help_text='Status of the transaction.', max_length=10)),
                ('payment_method', models.CharField(blank=True, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('bank_transfer', 'Bank Transfer')], help_text='Payment method used by the buyer.', max_length=20, null=True)),
                ('payment_date', models.DateTimeField(blank=True, help_text='Date and time when the payment was completed.', null=True)),
                ('transaction_reference', models.CharField(blank=True, help_text='Reference number provided by the third-party payment gateway.', max_length=255, null=True)),
                ('shipping_address', models.TextField(blank=True, help_text='Shipping address for the product.', null=True)),
                ('cancellation_reason', models.TextField(blank=True, help_text='Reason for transaction cancellation, if applicable.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the transaction was created.')),
            ],
        ),
    ]
