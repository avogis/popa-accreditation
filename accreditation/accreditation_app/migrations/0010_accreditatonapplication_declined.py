# Generated by Django 2.0.3 on 2018-03-13 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accreditation_app', '0009_auto_20180312_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='accreditatonapplication',
            name='declined',
            field=models.BooleanField(default=False),
        ),
    ]
