# Generated by Django 3.0.8 on 2020-08-10 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_post_sub_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
