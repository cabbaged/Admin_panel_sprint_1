# Generated by Django 3.1 on 2021-07-24 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20210724_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='type',
            field=models.CharField(max_length=20, verbose_name='тип'),
        ),
    ]