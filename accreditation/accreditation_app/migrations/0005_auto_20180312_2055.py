# Generated by Django 2.0.3 on 2018-03-12 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accreditation_app', '0004_accreditatonapplication_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accreditatonapplication',
            old_name='text',
            new_name='application',
        ),
    ]
