# Generated by Django 4.0.1 on 2022-03-09 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0014_contract_event_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]