# Generated by Django 3.1.4 on 2020-12-30 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_number',
            field=models.TextField(),
        ),
    ]
