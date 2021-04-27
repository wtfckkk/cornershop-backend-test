from django.contrib.auth.models import Group, Permission, User
from django.core.management.sql import emit_post_migrate_signal
from django.db import migrations


def add_group_permissions(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    emit_post_migrate_signal(2, False, 'default')

    role, created = Group.objects.get_or_create(name="employees")
    if created:
        role.permissions.add(Permission.objects.get(codename='view_order'))
        role.permissions.add(Permission.objects.get(codename='view_meal'))
        role.save()


def add_superuser(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    emit_post_migrate_signal(2, False, 'default')

    User.objects.create_superuser(username="nora", password="cornershop")


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0009_auto_20210426_2309'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions),
        migrations.RunPython(add_superuser),
    ]
