# Generated by Django 4.2.1 on 2023-05-25 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_prescription_advice_alter_prescription_cc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.appointment'),
        ),
    ]
