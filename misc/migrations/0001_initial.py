from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=100)),
                ('model', models.CharField(choices=[('lightweight', 'Lightweight'), ('middleweight', 'Middleweight'), ('cruiserweight', 'Cruiserweight'), ('heavyweight', 'Heavyweight')], default='middleweight', max_length=20)),
                ('weight_limit', models.FloatField()),
                ('battery_capacity', models.FloatField()),
                ('state', models.CharField(choices=[('IDLE', 'Idle'), ('LOADING', 'Loading'), ('LOADED', 'Loaded'), ('DELIVERING', 'Delivering'), ('DELIVERED', 'Delivered'), ('RETURNING', 'Returning')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('weight', models.FloatField()),
                ('code', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='images/medications')),
            ],
        ),
    ]
