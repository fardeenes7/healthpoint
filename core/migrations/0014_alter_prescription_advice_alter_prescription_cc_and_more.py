# Generated by Django 4.2.1 on 2023-05-25 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_appointment_note_alter_appointment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='advice',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='cc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='diagnosis',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='tx',
            field=models.TextField(blank=True, null=True),
        ),
    ]
