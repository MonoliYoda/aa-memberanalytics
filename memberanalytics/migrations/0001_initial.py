# Generated by Django 3.2.13 on 2022-04-28 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eveuniverse', '0007_evetype_description'),
        ('authentication', '0019_merge_20211026_0919'),
        ('eveonline', '0015_factions'),
    ]

    operations = [
        migrations.CreateModel(
            name='General',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('basic_access', 'Can access this app'),),
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('corporation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='mining_corporation', serialize=False, to='eveonline.evecorporationinfo')),
                ('character_ownership', models.ForeignKey(default=None, help_text='character used to sync this corporation from ESI', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to='authentication.characterownership')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterSessionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_id', models.IntegerField(null=True)),
                ('ship_type_id', models.IntegerField(null=True)),
                ('session_start', models.DateTimeField(default=None, help_text='Time this character last logged on', null=True)),
                ('session_end', models.DateTimeField(default=None, help_text='Time this character last logged off', null=True)),
                ('character', models.ForeignKey(help_text='EVE Character', on_delete=django.db.models.deletion.CASCADE, to='eveuniverse.eveentity')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_corp', models.DateTimeField(null=True)),
                ('tracking_since', models.DateTimeField(auto_now_add=True)),
                ('character', models.ForeignKey(help_text='EVE Character', on_delete=django.db.models.deletion.CASCADE, to='eveuniverse.eveentity')),
            ],
        ),
    ]
