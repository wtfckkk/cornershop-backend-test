# Generated by Django 3.0.8 on 2021-04-26 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0003_auto_20210425_1825'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SlackInstall',
        ),
        migrations.AddField(
            model_name='menu',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]