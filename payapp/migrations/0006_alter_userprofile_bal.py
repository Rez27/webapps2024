# Generated by Django 4.2.10 on 2024-04-10 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0005_alter_userprofile_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bal',
            field=models.FloatField(default=0),
        ),
    ]
