# Generated by Django 4.1.2 on 2022-12-13 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='dealer_code',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dealer_name', models.CharField(max_length=30)),
            ],
        ),
    ]