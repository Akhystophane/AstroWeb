# Generated by Django 4.1.4 on 2024-05-25 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='e_mail',
            field=models.EmailField(default='', max_length=200),
        ),
    ]