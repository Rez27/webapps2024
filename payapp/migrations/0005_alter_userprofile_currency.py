# Generated by Django 4.2.10 on 2024-04-09 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0004_rename_sender_notification_requester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='currency',
            field=models.CharField(choices=[('GBP', 'GBP'), ('USD', 'USD'), ('EUR', 'EUR')], default='GBP', max_length=3),
        ),
    ]
