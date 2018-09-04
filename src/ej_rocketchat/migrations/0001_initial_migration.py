# Generated by Django 2.0.6 on 2018-08-24 21:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RCAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='Username that identifies you in the Rocket.Chat platform.\nUse small names with letters and dashes such as @my-user-name.', max_length=50, validators=[django.core.validators.RegexValidator('^\\@?(\\w+-)*\\w+$', message='Username must consist of letters, numbers and dashes.')], verbose_name='Username')),
                ('password', models.CharField(blank=True, max_length=50, verbose_name='Password')),
                ('user_rc_id', models.CharField(max_length=50, verbose_name='Rocketchat user id')),
                ('auth_token', models.CharField(blank=True, max_length=50, verbose_name='Rocketchat user token')),
                ('account_data', jsonfield.fields.JSONField(blank=True, help_text='JSON-encoded data for user account.', null=True, verbose_name='Account data')),
                ('is_active', models.BooleanField(default=True, help_text='True for active Rocket.Chat accounts.', verbose_name='Is user active?')),
            ],
            options={
                'verbose_name': 'Rocket.Chat Account',
                'verbose_name_plural': 'Rocket.Chat Accounts',
                'permissions': [('can_create_account', 'Can login in the Rocket.Chat instance.')],
            },
        ),
        migrations.CreateModel(
            name='RCConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(default='http://localhost:3000', help_text='Public URL in which the Rocket.Chat instance is installed.', unique=True, verbose_name='Rocket.Chat URL')),
                ('api_url', models.URLField(blank=True, help_text='A private URL used only for API calls. Can be used to override the public URL if Rocket.Chat is available in an internal address in your network.', null=True, unique=True, verbose_name='Rocket.Chat private URL')),
                ('admin_username', models.CharField(default='ej-admin', help_text='Username for Rocket.Chat admin user', max_length=50, verbose_name='Admin username')),
                ('admin_id', models.CharField(help_text='Id string for the Rocket.Chat admin user.', max_length=50, verbose_name='Admin user id')),
                ('admin_token', models.CharField(help_text='Login token for the Rocket.Chat admin user.', max_length=50, verbose_name='Login token')),
                ('is_active', models.BooleanField(default=True, help_text='Set to false to temporarily disable RocketChat integration.', verbose_name='Is active')),
            ],
            options={
                'verbose_name': 'Rocket.Chat Configuration',
                'verbose_name_plural': 'Rocket.Chat Configurations',
            },
        ),
        migrations.AddField(
            model_name='rcaccount',
            name='config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ej_rocketchat.RCConfig'),
        ),
        migrations.AddField(
            model_name='rcaccount',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rocketchat_subscription', to=settings.AUTH_USER_MODEL),
        ),
    ]
