# Generated by Django 3.2.7 on 2021-09-17 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_rename_type_watering_watering_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterModelOptions(
            name='watering',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='watering',
            name='date',
            field=models.DateField(verbose_name='watering date'),
        ),
    ]
