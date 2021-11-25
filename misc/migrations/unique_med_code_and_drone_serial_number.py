import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0002_model_validators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='serial_number',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a valid value. Allowed only letters, underscores, dashes and numbers.', regex='^[a-zA-Z0-9]([a-zA-Z0-9_-])+$')]),
        ),
        migrations.AlterField(
            model_name='medication',
            name='code',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a valid value. Allowed only upper case letters, underscores and numbers.', regex='^[A-Z0-9]([A-Z0-9_])+$')]),
        ),
    ]
