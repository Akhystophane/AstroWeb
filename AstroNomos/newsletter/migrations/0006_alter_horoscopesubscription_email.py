# Generated by Django 4.1.4 on 2024-05-25 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0005_alter_horoscopesubscription_zodiac_sign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horoscopesubscription',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]
