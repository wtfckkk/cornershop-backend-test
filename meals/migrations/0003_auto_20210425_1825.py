# Generated by Django 3.0.8 on 2021-04-25 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_auto_20210425_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='country',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
