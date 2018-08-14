# Generated by Django 2.0.8 on 2018-08-14 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ej_conversations', '0009_auto_20180730_1437'),
        ('ej_clusters', '0004_stereotype_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='stereotype',
            name='conversation',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='stereotypes', to='ej_conversations.Conversation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stereotype',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Name'),
        ),
        migrations.RemoveField(
            model_name='stereotype',
            name='owner',
        ),
        migrations.AlterUniqueTogether(
            name='stereotype',
            unique_together={('name', 'conversation')},
        ),
    ]