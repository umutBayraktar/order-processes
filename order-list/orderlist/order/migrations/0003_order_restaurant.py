# Generated by Django 4.0.1 on 2022-01-18 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
        ('order', '0002_rename_orders_order_food_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='restaurant.restaurant'),
        ),
    ]
