# Generated by Django 4.0.2 on 2022-03-18 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_product_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='final_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
