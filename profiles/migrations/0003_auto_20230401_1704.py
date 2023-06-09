# Generated by Django 3.2.12 on 2023-04-01 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='profiles/default.png', upload_to='profiles'),
        ),
    ]
