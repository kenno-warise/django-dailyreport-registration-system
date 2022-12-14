# Generated by Django 3.2.16 on 2022-10-23 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0004_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='break_time',
            field=models.TimeField(blank=True, null=True, verbose_name='休憩時間'),
        ),
        migrations.AlterField(
            model_name='work',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='業務内容'),
        ),
        migrations.AlterField(
            model_name='work',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='日付'),
        ),
        migrations.AlterField(
            model_name='work',
            name='end_time',
            field=models.TimeField(blank=True, null=True, verbose_name='退勤時間'),
        ),
        migrations.AlterField(
            model_name='work',
            name='start_time',
            field=models.TimeField(blank=True, null=True, verbose_name='出勤時間'),
        ),
    ]
