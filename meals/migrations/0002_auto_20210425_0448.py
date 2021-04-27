# Generated by Django 3.0.8 on 2021-04-24 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlackInstall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(max_length=20)),
                ('user_access_token', models.CharField(max_length=100)),
                ('bot_access_token', models.CharField(max_length=100)),
                ('channel_id', models.CharField(max_length=30)),
                ('channel', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='menu',
        ),
        migrations.AddField(
            model_name='employee',
            name='slack_user',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='meal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='meals.Meal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='rate',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='meals',
            field=models.ManyToManyField(to='meals.Meal'),
        ),
    ]
