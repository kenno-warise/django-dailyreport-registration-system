# Generated by Django 3.2.16 on 2022-10-28 11:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0008_alter_user_user_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_no',
            field=models.CharField(error_messages={'unique': '既に使用されている番号です'}, help_text='4桁で番号を入力。', max_length=4, unique=True, validators=[django.core.validators.MinLengthValidator(4), django.core.validators.RegexValidator(message='4桁の社員番号を入力してください。', regex='\\d{4}')], verbose_name='社員番号'),
        ),
    ]
