# Generated by Django 4.2.1 on 2023-05-27 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_rename_doses_medication_dosage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prescription',
            old_name='next_visit',
            new_name='followup',
        ),
    ]