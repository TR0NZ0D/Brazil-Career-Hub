# Generated by Django 4.1.4 on 2022-12-20 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_admins', '0003_alter_apiadmin_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiadmin',
            name='user',
            field=models.OneToOneField(error_messages={'unique': 'This user already has a token.'}, help_text='The user that own this token. Please check if user is admin before giving him a token.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]