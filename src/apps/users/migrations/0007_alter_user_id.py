# Generated by Django 5.2.1 on 2025-06-17 15:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.UUID('f6bb8e10-1e81-4eb7-b05b-2ce2b252207b'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
