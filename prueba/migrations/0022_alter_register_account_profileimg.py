# Generated by Django 4.1.7 on 2023-04-22 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prueba', '0021_register_account_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_account',
            name='profileimg',
            field=models.ImageField(default='', upload_to='post_images/'),
        ),
    ]
