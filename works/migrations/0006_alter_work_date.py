# Generated by Django 3.2.16 on 2022-10-23 03:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0005_auto_20221023_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='日付'),
            preserve_default=False,
        ),
    ]
