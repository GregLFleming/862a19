# Generated by Django 3.2.4 on 2022-01-18 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger_backend', '0007_message_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='lastRead',
            field=models.BooleanField(default=False),
        ),
    ]