# Generated by Django 4.2.5 on 2023-10-03 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_customuser_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to='media/images/profile'),
        ),
    ]
