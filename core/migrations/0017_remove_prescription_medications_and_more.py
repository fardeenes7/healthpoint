# Generated by Django 4.2.1 on 2023-05-26 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_prescription_appointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='medications',
        ),
        migrations.AddField(
            model_name='medication',
            name='prescription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medications', to='core.prescription'),
        ),
    ]
