# Generated by Django 4.1.2 on 2022-11-05 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='status',
            field=models.CharField(max_length=10),
        ),
    ]
