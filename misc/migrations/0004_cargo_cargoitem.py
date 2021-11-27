from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0003_unique_med_code_and_drone_serial_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drone', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cargo', to='misc.drone')),
            ],
        ),
        migrations.CreateModel(
            name='CargoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=0)),
                ('cargo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='misc.cargo')),
                ('med', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='misc.medication')),
            ],
        ),
    ]
