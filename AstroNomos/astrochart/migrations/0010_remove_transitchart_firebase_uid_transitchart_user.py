# Generated by Django 4.2.13 on 2024-09-17 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('astrochart', '0009_transitchart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transitchart',
            name='firebase_uid',
        ),
        migrations.AddField(
            model_name='transitchart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, null=True),

        ),
    ]
