# Generated by Django 5.1 on 2024-08-30 16:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_post_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='preview',
            field=models.TextField(blank=True, help_text='Optional preview text for the post.', validators=[django.core.validators.MaxLengthValidator(limit_value=300)]),
        ),
    ]
