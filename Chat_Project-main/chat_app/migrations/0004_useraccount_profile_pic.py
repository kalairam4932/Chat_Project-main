# Generated by Django 5.0.6 on 2024-06-08 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0003_alter_message_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='profile_pic',
            field=models.ImageField(default='default_profile.jpg', upload_to='profile_pics'),
        ),
    ]
