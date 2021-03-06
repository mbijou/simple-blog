# Generated by Django 3.0.8 on 2020-08-11 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_auto_20200811_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('PARAGRAPH', 'Paragraph'), ('SUBTITLE', 'Subtitle'), ('IMAGE', 'Image'), ('BLOCKQUOTE', 'Blockquote')], default='PARAGRAPH', max_length=200),
        ),
    ]
