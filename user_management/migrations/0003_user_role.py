# Generated by Django 4.0.4 on 2022-05-08 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_alter_user_options_alter_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default='student', max_length=32),
        ),
    ]
