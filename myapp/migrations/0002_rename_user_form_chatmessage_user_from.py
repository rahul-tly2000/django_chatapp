# Generated by Django 4.0.3 on 2022-04-05 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatmessage',
            old_name='user_form',
            new_name='user_from',
        ),
    ]