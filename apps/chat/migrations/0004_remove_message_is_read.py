# Generated by Django 4.2 on 2025-03-18 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_is_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='is_read',
        ),
    ]
