# Generated by Django 4.2.10 on 2024-04-19 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0016_rename_amount_transaction_sent_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='received_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sent_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
