# Generated by Django 4.2.1 on 2023-05-26 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_prescription_medications_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medication',
            old_name='doses',
            new_name='dosage',
        ),
    ]
