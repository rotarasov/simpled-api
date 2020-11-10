# Generated by Django 3.1.2 on 2020-11-09 17:11

import cloudinary.models
from django.db import migrations
import users.services


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201028_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=cloudinary.models.CloudinaryField(default=users.services.get_default_user_image, max_length=255, validators=[users.services.validate_user_image], verbose_name='profile image'),
        ),
    ]