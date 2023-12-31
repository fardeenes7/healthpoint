# Generated by Django 4.2.1 on 2023-05-24 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_workspace_doctor_workplace'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('schedule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='core.schedules')),
            ],
        ),
    ]
