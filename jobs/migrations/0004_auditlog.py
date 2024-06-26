# Generated by Django 5.0.6 on 2024-05-19 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_jobapplication_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('resource_name', models.CharField(max_length=100)),
                ('action', models.CharField(max_length=10)),
                ('payload', models.JSONField()),
            ],
        ),
    ]
