# Generated by Django 5.2.4 on 2025-07-31 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_meeting_date_and_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
