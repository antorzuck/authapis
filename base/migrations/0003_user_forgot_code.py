# Generated by Django 4.0.5 on 2022-10-14 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_user_birth_date_alter_user_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='forgot_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
