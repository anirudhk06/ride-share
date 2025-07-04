# Generated by Django 5.2.1 on 2025-06-16 18:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_managers_remove_user_avatar_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='lastname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login_medium',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login_uagent',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_logout_time',
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.UUID('6a784a8e-3042-4e45-b440-7582beb990e3'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
