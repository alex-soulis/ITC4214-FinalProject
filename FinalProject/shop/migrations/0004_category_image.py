# Generated by Django 5.1.7 on 2025-04-19 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_category_slug_product_slug_review_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
    ]
