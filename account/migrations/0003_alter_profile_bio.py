# Generated by Django 3.2.7 on 2021-09-23 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210923_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
