# Generated by Django 2.0.3 on 2018-03-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accreditation_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accreditatonapplication',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='accreditatonapplication',
            name='first_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='accreditatonapplication',
            name='last_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
