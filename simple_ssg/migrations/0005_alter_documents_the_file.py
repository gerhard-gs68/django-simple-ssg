# Generated by Django 4.0.5 on 2022-08-08 14:14

from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    dependencies = [
        ('simple_ssg', '0004_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='the_file',
            field=models.FileField(upload_to=pathlib.PurePosixPath('/Users/gerhard/Desktop/myprojects/simple-ssg/s4sensors/media/documents')),
        ),
    ]