# Generated by Django 4.2.14 on 2024-09-17 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astrochart', '0003_react_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='react',
            name='firebase_uid',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
