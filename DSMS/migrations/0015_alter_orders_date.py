# Generated by Django 4.0.6 on 2022-09-08 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DSMS', '0014_orders_rejected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='date',
            field=models.DateTimeField(),
        ),
    ]