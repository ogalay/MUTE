# Generated by Django 2.2.7 on 2020-01-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200104_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
