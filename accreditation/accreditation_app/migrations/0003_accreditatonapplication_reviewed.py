# Generated by Django 2.0.3 on 2018-03-12 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accreditation_app', '0002_auto_20180312_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='accreditatonapplication',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
    ]
