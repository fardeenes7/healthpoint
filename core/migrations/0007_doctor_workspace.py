# Generated by Django 4.2.1 on 2023-05-22 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_doctor_email_remove_patient_email_doctor_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='workspace',
            field=models.CharField(default='N/A', max_length=100),
        ),
    ]
