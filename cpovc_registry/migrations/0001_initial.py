# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OVCCheckin',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('is_ovc', models.BooleanField(default=True)),
                ('is_void', models.BooleanField(default=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'ovc_checkin',
            },
        ),
        migrations.CreateModel(
            name='OVCHouseHold',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('members', models.CharField(max_length=200)),
                ('is_void', models.BooleanField(default=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'reg_household',
            },
        ),
        migrations.CreateModel(
            name='OVCSibling',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('other_names', models.CharField(default=None, max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('sex_id', models.CharField(max_length=4)),
                ('class_level', models.CharField(max_length=4, null=True)),
                ('remarks', models.CharField(max_length=250, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ovc_sibling',
            },
        ),
        migrations.CreateModel(
            name='PersonsMaster',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('person_type', models.CharField(max_length=5, null=True)),
                ('system_id', models.CharField(max_length=100, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'reg_person_master',
            },
        ),
        migrations.CreateModel(
            name='RegBiometric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('left_iris', models.BinaryField()),
                ('right_iris', models.BinaryField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reg_biometric',
                'verbose_name': 'Persons Biometric',
                'verbose_name_plural': 'Persons Biometrics',
            },
        ),
        migrations.CreateModel(
            name='RegOrgUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('org_unit_id_vis', models.CharField(max_length=12)),
                ('org_unit_name', models.CharField(max_length=255)),
                ('org_unit_type_id', models.CharField(max_length=4)),
                ('date_operational', models.DateField(null=True, blank=True)),
                ('date_closed', models.DateField(null=True, blank=True)),
                ('handle_ovc', models.BooleanField(default=False)),
                ('is_void', models.BooleanField(default=False)),
                ('parent_org_unit_id', models.IntegerField(null=True, blank=True)),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'reg_org_unit',
                'verbose_name': 'Organisational Units Registry',
                'verbose_name_plural': 'Organisational Units Registries',
            },
        ),
        migrations.CreateModel(
            name='RegOrgUnitContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_detail_type_id', models.CharField(max_length=20)),
                ('contact_detail', models.CharField(max_length=255)),
                ('is_void', models.BooleanField(default=False)),
                ('org_unit', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
            ],
            options={
                'db_table': 'reg_org_units_contact',
            },
        ),
        migrations.CreateModel(
            name='RegOrgUnitExternalID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier_type_id', models.CharField(max_length=4)),
                ('identifier_value', models.CharField(max_length=255, null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('org_unit', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
            ],
            options={
                'db_table': 'reg_org_units_external_ids',
            },
        ),
        migrations.CreateModel(
            name='RegOrgUnitGeography',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_linked', models.DateField(null=True)),
                ('date_delinked', models.DateField(null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('area', models.ForeignKey(to='cpovc_main.SetupGeography')),
                ('org_unit', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
            ],
            options={
                'db_table': 'reg_org_units_geo',
            },
        ),
        migrations.CreateModel(
            name='RegOrgUnitsAuditTrail',
            fields=[
                ('transaction_id', models.AutoField(serialize=False, primary_key=True)),
                ('transaction_type_id', models.CharField(max_length=4, null=True, db_index=True)),
                ('interface_id', models.CharField(max_length=4, null=True, db_index=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('meta_data', models.TextField(null=True)),
                ('app_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('org_unit', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
            ],
            options={
                'db_table': 'reg_org_units_audit_trail',
                'verbose_name': 'Org Units Audit Trail',
                'verbose_name_plural': 'Org Units Audit Trails',
            },
        ),
        migrations.CreateModel(
            name='RegPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation', models.CharField(max_length=25, null=True)),
                ('first_name', models.CharField(max_length=255)),
                ('other_names', models.CharField(max_length=255, null=True)),
                ('surname', models.CharField(default=None, max_length=255)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('des_phone_number', models.IntegerField(default=None, null=True, blank=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('date_of_death', models.DateField(default=None, null=True, blank=True)),
                ('sex_id', models.CharField(max_length=4, choices=[(b'SMAL', b'Male'), (b'SFEM', b'Female')])),
                ('is_void', models.BooleanField(default=False)),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'reg_person',
                'verbose_name': 'Persons Registry',
                'verbose_name_plural': 'Persons Registries',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsAuditTrail',
            fields=[
                ('transaction_id', models.AutoField(serialize=False, primary_key=True)),
                ('transaction_type_id', models.CharField(max_length=4, null=True, db_index=True)),
                ('interface_id', models.CharField(max_length=4, null=True, db_index=True)),
                ('date_recorded_paper', models.DateField(null=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('meta_data', models.TextField(null=True)),
                ('app_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
                ('person_recorded_paper', models.ForeignKey(related_name='person_recorded_paper', to='cpovc_registry.RegPerson', null=True)),
            ],
            options={
                'db_table': 'reg_persons_audit_trail',
                'verbose_name': 'Persons Audit Trail',
                'verbose_name_plural': 'Persons Audit Trails',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsBeneficiaryIds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beneficiary_id', models.CharField(max_length=10, null=True)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_beneficiary_ids',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_detail_type_id', models.CharField(max_length=4)),
                ('contact_detail', models.CharField(max_length=255)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_contact',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsExternalIds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier_type_id', models.CharField(max_length=4)),
                ('identifier', models.CharField(max_length=255)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_external_ids',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsGeo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area_type', models.CharField(max_length=4)),
                ('date_linked', models.DateField(null=True)),
                ('date_delinked', models.DateField(null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('area', models.ForeignKey(to='cpovc_main.SetupGeography')),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_geo',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsGuardians',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relationship', models.CharField(max_length=5)),
                ('date_linked', models.DateField(null=True)),
                ('date_delinked', models.DateField(null=True)),
                ('child_headed', models.BooleanField(default=False)),
                ('is_void', models.BooleanField(default=False)),
                ('child_person', models.ForeignKey(related_name='child_person', to='cpovc_registry.RegPerson')),
                ('guardian_person', models.ForeignKey(related_name='guardian_person', to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_guardians',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsOrgUnits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_linked', models.DateField(null=True)),
                ('date_delinked', models.DateField(null=True)),
                ('primary_unit', models.BooleanField(default=False)),
                ('reg_assistant', models.BooleanField(default=False)),
                ('is_void', models.BooleanField(default=False)),
                ('org_unit', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_org_units',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsSiblings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_linked', models.DateField(null=True)),
                ('date_delinked', models.DateField(null=True)),
                ('remarks', models.TextField(null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('child_person', models.ForeignKey(related_name='child_sibling', to='cpovc_registry.RegPerson')),
                ('sibling_person', models.ForeignKey(related_name='sibling_person', to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_siblings',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person_type_id', models.CharField(max_length=4)),
                ('date_began', models.DateField(null=True)),
                ('date_ended', models.DateField(default=None, null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_types',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsWorkforceIds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('workforce_id', models.CharField(max_length=8, null=True)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_workforce_ids',
            },
        ),
        migrations.AddField(
            model_name='personsmaster',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson', null=True),
        ),
        migrations.AddField(
            model_name='ovcsibling',
            name='cpims',
            field=models.ForeignKey(related_name='ovc_cpims', to='cpovc_registry.RegPerson', null=True),
        ),
        migrations.AddField(
            model_name='ovcsibling',
            name='person',
            field=models.ForeignKey(related_name='ovc_sibling', to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovchousehold',
            name='index_child',
            field=models.ForeignKey(related_name='index_child', to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovccheckin',
            name='org_unit',
            field=models.ForeignKey(to='cpovc_registry.RegOrgUnit', null=True),
        ),
        migrations.AddField(
            model_name='ovccheckin',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovccheckin',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
