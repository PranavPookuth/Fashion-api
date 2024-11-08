# Generated by Django 5.1.1 on 2024-11-05 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile_number', models.CharField(max_length=15, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('otp_secret_key', models.CharField(blank=True, max_length=32, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('road_name', models.TextField(default='road_name')),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('DOB', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
