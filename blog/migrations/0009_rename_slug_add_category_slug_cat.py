# Generated by Django 3.2.6 on 2021-09-07 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210907_1332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='add_category',
            old_name='slug',
            new_name='slug_cat',
        ),
    ]
