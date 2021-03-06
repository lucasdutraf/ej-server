# Generated by Django 2.1.2 on 2018-11-19 15:26

import autoslug.fields
import boogie.fields.enum_field
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ej_notifications.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('purpose', boogie.fields.enum_field.EnumField(ej_notifications.models.Purpose, default=ej_notifications.models.Purpose(0), verbose_name='Purpose')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='channel_owner', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.CharField(max_length=250)),
                ('link', models.CharField(blank=True, max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(default='pending', max_length=100)),
                ('target', models.IntegerField(blank=True, default=0)),
                ('channel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ej_notifications.Channel')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ej_notifications.Channel')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ej_notifications.Message')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_option', boogie.fields.enum_field.EnumField(ej_notifications.models.NotificationOptions, default=ej_notifications.models.NotificationOptions(0), verbose_name='Notification options')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='raw_notificationsconfig', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
