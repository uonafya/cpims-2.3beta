# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
        ('cpovc_main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coreservices',
            name='beneficiary_person',
            field=models.ForeignKey(related_name='service_beneficiary', to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='coreservices',
            name='workforce_person',
            field=models.ForeignKey(related_name='service_workforce', to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='coreencountersnotes',
            name='beneficiary_person',
            field=models.ForeignKey(related_name='encounter_n_beneficiary', to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='coreencountersnotes',
            name='encounter',
            field=models.ForeignKey(to='cpovc_main.CoreEncounters'),
        ),
        migrations.AddField(
            model_name='coreencountersnotes',
            name='workforce_person',
            field=models.ForeignKey(related_name='encounter_n_workforce', to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='coreencounters',
            name='beneficiary_person',
            field=models.ForeignKey(related_name='encounter_beneficiary', to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='coreencounters',
            name='workforce_person',
            field=models.ForeignKey(related_name='encounter_workforce', to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='coreadverseconditions',
            name='beneficiary_person',
            field=models.ForeignKey(related_name='adverse_beneficiary', to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='adminuploadforms',
            name='form',
            field=models.ForeignKey(to='cpovc_main.Forms'),
        ),
        migrations.AddField(
            model_name='adminpreferences',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AlterUniqueTogether(
            name='reportssetsorgunits',
            unique_together=set([('set', 'org_unit_id')]),
        ),
    ]
