# Generated by Django 4.0.5 on 2022-07-02 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='users',
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(related_name='roles', to='dashboard_app.permission'),
        ),
    ]