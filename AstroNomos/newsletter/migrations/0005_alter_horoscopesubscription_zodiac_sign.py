# Generated by Django 4.1.4 on 2024-05-25 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0004_alter_horoscopesubscription_zodiac_sign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horoscopesubscription',
            name='zodiac_sign',
            field=models.CharField(choices=[('aries', '♈ Aries'), ('taurus', '♉ Taurus'), ('gemini', '♊ Gemini'), ('cancer', '♋ Cancer'), ('leo', '♌ Leo'), ('virgo', '♍ Virgo'), ('libra', '♎ Libra'), ('scorpio', '♏ Scorpio'), ('sagittarius', '♐ Sagittarius'), ('capricorn', '♑ Capricorn'), ('aquarius', '♒ Aquarius'), ('pisces', '♓ Pisces')], default='aries', max_length=20),
        ),
    ]
