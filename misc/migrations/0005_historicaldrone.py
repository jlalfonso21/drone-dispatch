from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('misc', '0004_cargo_cargoitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalDrone',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('serial_number', models.CharField(db_index=True, max_length=100, validators=[django.core.validators.RegexValidator(message='Enter a valid value. Allowed only letters, underscores, dashes and numbers.', regex='^[a-zA-Z0-9]([a-zA-Z0-9_-])+$')])),
                ('model', models.CharField(choices=[('lightweight', 'Lightweight'), ('middleweight', 'Middleweight'), ('cruiserweight', 'Cruiserweight'), ('heavyweight', 'Heavyweight')], default='middleweight', max_length=20)),
                ('weight_limit', models.FloatField(help_text='Weight in grams (g). 500g max.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)])),
                ('battery_capacity', models.FloatField(default=100.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('state', models.CharField(choices=[('IDLE', 'Idle'), ('LOADING', 'Loading'), ('LOADED', 'Loaded'), ('DELIVERING', 'Delivering'), ('DELIVERED', 'Delivered'), ('RETURNING', 'Returning')], default='IDLE', max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical drone',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
