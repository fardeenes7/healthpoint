# Generated by Django 4.2.1 on 2023-05-25 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_prescription_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescription', to='core.appointment'),
        ),
    ]
