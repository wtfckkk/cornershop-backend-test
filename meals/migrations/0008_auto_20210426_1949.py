# Generated by Django 3.0.8 on 2021-04-26 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0007_order_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='rate',
        ),
        migrations.AlterField(
            model_name='order',
            name='customization',
            field=models.TextField(blank=True),
        ),
    ]