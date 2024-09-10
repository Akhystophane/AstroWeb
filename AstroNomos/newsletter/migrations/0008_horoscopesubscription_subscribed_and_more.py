# Generated by Django 4.2.14 on 2024-09-10 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0007_alter_horoscopesubscription_zodiac_sign'),
    ]

    operations = [
        migrations.AddField(
            model_name='horoscopesubscription',
            name='subscribed',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='horoscopesubscription',
            name='unsubscribe_token',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]
