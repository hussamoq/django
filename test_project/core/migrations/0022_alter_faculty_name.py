# Generated by Django 4.0.3 on 2022-05-20 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_faculty_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
