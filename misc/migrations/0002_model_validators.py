import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='battery_capacity',
            field=models.FloatField(default=100.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='drone',
            name='serial_number',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Enter a valid value. Allowed only letters, underscores, dashes and numbers.', regex='^[a-zA-Z0-9]([a-zA-Z0-9_-])+$')]),
        ),
        migrations.AlterField(
            model_name='drone',
            name='state',
            field=models.CharField(choices=[('IDLE', 'Idle'), ('LOADING', 'Loading'), ('LOADED', 'Loaded'), ('DELIVERING', 'Delivering'), ('DELIVERED', 'Delivered'), ('RETURNING', 'Returning')], default='IDLE', max_length=20),
        ),
        migrations.AlterField(
            model_name='drone',
            name='weight_limit',
            field=models.FloatField(help_text='Weight in grams (g). 500g max.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
        ),
        migrations.AlterField(
            model_name='medication',
            name='code',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Enter a valid value. Allowed only upper case letters, underscores and numbers.', regex='^[A-Z0-9]([A-Z0-9_])+$')]),
        ),
        migrations.AlterField(
            model_name='medication',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/medications'),
        ),
        migrations.AlterField(
            model_name='medication',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Enter a valid value. Allowed only letters, underscores, dashes and numbers.', regex='^[a-zA-Z0-9]([a-zA-Z0-9_-])+$')]),
        ),
        migrations.AlterField(
            model_name='medication',
            name='weight',
            field=models.FloatField(help_text='Weight in grams (g).', validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
