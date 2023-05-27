# Generated by Django 4.2 on 2023-04-14 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.CharField(max_length=150)),
                ('place', models.CharField(max_length=50)),
                ('pin_code', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.packages')),
            ],
        ),
    ]