# Generated by Django 4.1.4 on 2022-12-20 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_admins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiadmin',
            name='token',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='API Token'),
        ),
        migrations.AlterField(
            model_name='apiadmin',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
