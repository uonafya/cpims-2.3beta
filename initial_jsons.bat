python manage.py makemigrations
python manage.py migrate cpovc_auth
python manage.py migrate
python manage.py loaddata cpovc_auth\fixtures\initial_data.json
python manage.py loaddata cpovc_main\fixtures\initial_user.json
python manage.py loaddata cpovc_main\fixtures\initial_geo.json
python manage.py loaddata cpovc_main\fixtures\list_general.csv.json
python manage.py loaddata cpovc_main\fixtures\initial_facility1.json
python manage.py loaddata cpovc_main\fixtures\initial_facility2.json
python manage.py loaddata cpovc_main\fixtures\initial_facility3.json

python manage.py loaddata cpovc_main\fixtures\olmis_forms.csv.json
python manage.py loaddata cpovc_main\fixtures\olmis_assessment.csv.json
python manage.py loaddata cpovc_main\fixtures\olmis_household_assessment_3.json
python manage.py loaddata cpovc_main\fixtures\olmis_registry.json
python manage.py loaddata cpovc_main\fixtures\eligibility.json
python manage.py loaddata cpovc_main\fixtures\olmis_services.csv.json
python manage.py loaddata cpovc_main\fixtures\ovc_form_type_id.json
python manage.py createsuperuser

python manage.py loaddata cpovc_main\fixtures\initial_org_unit.csv.json
python manage.py loaddata cpovc_main\fixtures\initial_org_unit_contact.csv.json
python manage.py loaddata cpovc_main\fixtures\initial_org_unit_geo.csv.json
python manage.py loaddata cpovc_main\fixtures\initial_persons.csv.json
python manage.py loaddata cpovc_main\fixtures\initial_person_type.csv.json
python manage.py loaddata cpovc_main\fixtures\initial_persons_externalids.csv.json
python manage.py loaddata cpovc_main\fixtures\initial_persons_geo.csv.json
python manage.py loaddata cpovc_main\fixtures\initial_persons_org_units.csv.json

python manage.py loaddata cpovc_forms\fixtures\ovc_care_forms.json
python manage.py loaddata cpovc_forms\fixtures\ovc_care_questions.json
python manage.py loaddata cpovc_forms\fixtures\form1b_revised.json
python manage.py loaddata cpovc_forms\fixtures\form1a_revised_assessments.json
python manage.py loaddata cpovc_forms\fixtures\olmis_assessment_revised.csv.json
python manage.py loaddata cpovc_forms\fixtures\olmis_services_revised.csv.json
python manage.py loaddata cpovc_forms\fixtures\case_plan_fixtures.csv.json


