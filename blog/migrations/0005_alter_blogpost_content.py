# Generated by Django 4.2.5 on 2023-10-03 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_tag_slug_alter_blogpost_slug_alter_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=models.TextField(max_length=2000),
        ),
    ]
