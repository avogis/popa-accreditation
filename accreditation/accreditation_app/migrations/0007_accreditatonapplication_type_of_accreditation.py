# Generated by Django 2.0.3 on 2018-03-12 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accreditation_app', '0006_accreditatonapplication_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='accreditatonapplication',
            name='type_of_accreditation',
            field=models.CharField(choices=[('photo', 'Photo Pass'), ('jounalist', 'Journalist Pass'), ('festival', 'Festival Pass')], default='photo', max_length=9),
        ),
    ]