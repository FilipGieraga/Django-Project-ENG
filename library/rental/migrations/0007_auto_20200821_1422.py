# Generated by Django 3.0.7 on 2020-08-21 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0006_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(max_length=15, null=True),
        ),
    ]