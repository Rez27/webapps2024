# Generated by Django 4.2.10 on 2024-04-10 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0006_alter_userprofile_bal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bal',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
