# Generated by Django 5.2 on 2025-04-16 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
