# Generated by Django 4.0.4 on 2022-08-26 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_card_quantity_alter_product_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
