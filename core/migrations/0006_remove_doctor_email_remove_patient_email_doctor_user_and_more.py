# Generated by Django 4.2.1 on 2023-05-21 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_remove_doctor_fees_remove_doctor_first_fees_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='email',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='email',
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
