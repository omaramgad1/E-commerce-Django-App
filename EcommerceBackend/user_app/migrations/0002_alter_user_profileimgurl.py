# Generated by Django 4.2 on 2023-05-24 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profileImgUrl',
            field=models.ImageField(blank=True, upload_to='profileImages/'),
        ),
    ]
