# Generated by Django 2.0.7 on 2019-05-18 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0014_auto_20190515_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='to_be_notified',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_notify', to=settings.AUTH_USER_MODEL),
        ),
    ]
